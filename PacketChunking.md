# Python Client Packet Chunking Implementation

## Overview

The Python ft-py client has been updated to properly handle UDP packet size limitations by automatically splitting large frames into multiple packets. This enables support for large geometries (320x64, 64x64, etc.) on systems where the UDP datagram limit is smaller than the full frame size.

## Problem

The original Python code attempted to send entire frames as single UDP packets, which failed with `EMSGSIZE` (errno 40) on systems with UDP limits smaller than 65507 bytes. On macOS (and likely other systems), the default UDP datagram limit is 9216 bytes.

For example:
- 64x64 frame: 12,308 bytes → exceeds 9216 byte system limit → EMSGSIZE error
- 320x64 frame: 61,440 bytes → far exceeds system limit → EMSGSIZE error

## Solution: Auto-Detection and Multi-Packet Tiling

### 1. System UDP Limit Detection

**File**: `flaschen_taschen/client/canvas.py`

Added `_get_max_udp_size()` function that:
- Checks `FT_UDP_SIZE` environment variable (if set)
- Queries system via `socket.SO_SNDBUF` (actual system limit)
- Falls back to 65507 if detection fails

```python
def _get_max_udp_size() -> int:
    """Get the maximum UDP datagram size for this system."""
    if 'FT_UDP_SIZE' in os.environ:
        return int(os.environ['FT_UDP_SIZE'])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            return udp_size
        finally:
            s.close()
    except Exception:
        pass

    return 65507
```

### 2. Multi-Packet Tiling

**File**: `flaschen_taschen/client/canvas.py`

The `_send_tiled()` method (and `send_layer()`) split large frames into multiple packets:

```python
max_udp_size = _get_max_udp_size()
header_reserve = 64
row_size = 3 * self.config.width
max_rows_per_packet = (max_udp_size - header_reserve) // row_size

# Split frame into tiles
while tile_offset < height:
    send_height = min(max_rows_per_packet, height - tile_offset)
    tile_pixels = rgb_pixels[tile_offset:tile_offset + send_height]

    # Each tile has its own PPM packet with adjusted y_offset
    ppm_data = PPMFormatter.encode(
        tile_pixels,
        x_offset=self.config.x_offset,
        y_offset=self.config.y_offset + tile_offset,
        layer=self.config.layer,
    )

    success = self.connection.send_frame(ppm_data, force=force)
    tile_offset += send_height
```

### 3. PPM Format with Layer Metadata

**File**: `flaschen_taschen/client/ppm_formatter.py`

Updated to include FlaschenTaschen metadata in PPM header comment (not as footer):

```
P6
<width> <height>
#FT: <x_offset> <y_offset> <layer>
255
[binary RGB pixel data]
```

This format:
- Puts metadata in PPM header comment `#FT:` (matching C++ implementation)
- Includes y_offset for tile positioning within layer
- Allows servers to composite multi-packet sequences correctly

## Example: 64x64 Frame on System with 9216 UDP Limit

### Calculation
- row_size = 3 × 64 = 192 bytes
- max_rows_per_packet = (9216 - 64) / 192 = 47 rows
- Total rows: 64, needs 2 packets

### Packets Sent

**Packet 1** (rows 0-46):
- Dimensions: 64×47
- Size: 9049 bytes
- Header: `#FT: 0 0 10` (layer 10, y_offset 0)

**Packet 2** (rows 47-63):
- Dimensions: 64×17
- Size: 3290 bytes
- Header: `#FT: 0 47 10` (layer 10, y_offset 47)

Server receives both packets and composites them at y_offset 0 and y_offset 47 into the same layer.

## Files Modified

1. **canvas.py**
   - Added `import os` and `import socket`
   - Added `_get_max_udp_size()` function
   - Updated `_send_tiled()` to use dynamic UDP size
   - Updated `send_layer()` to use dynamic UDP size

2. **ppm_formatter.py**
   - Modified `encode()` to put metadata in header comment
   - Removed footer-based metadata
   - Updated `decode()` to parse metadata from header comment

## Compatibility

### Environment Variables
- `FT_UDP_SIZE`: Optional override for UDP packet size limit
  - Example: `FT_UDP_SIZE=9216 python demo.py`
  - If not set, auto-detects from system

### Server Requirements
For proper multi-packet support, servers must:
1. Parse `#FT:` comment from PPM header
2. Extract x_offset, y_offset, and layer values
3. Composite tiles into the correct layer at correct y position
4. NOT clear the layer between packets of same sequence

## Testing

### Test 1: System with 9216 UDP Limit
```bash
python -m flaschen_taschen.demos.life -g 64x64 -h localhost -l 7 -t 30
```
Should display smooth animation without clearing between packets.

### Test 2: Large Geometry (320x64)
```bash
python -m flaschen_taschen.demos.plasma -g 320x64 -h localhost -l 5 -t 30
```
Should display full 320×64 animation with proper multi-packet compositing.

### Test 3: Debugger Fill Mode
```bash
python3 << 'EOF'
from flaschen_taschen.debugger import DisplayDebugger, Mode
from flaschen_taschen.client.config import Config

config = Config()
config.width = 64
config.height = 64
config.host = "localhost"
config.layer = 7

debugger = DisplayDebugger(mode=Mode.FILL, config=config)
debugger.run(timeout=30, delay_ms=100)
EOF
```
Should show solid color fill (all 4096 pixels) cycling through palette.

## Performance Notes

Multi-packet transmission may be slower than single-packet:
- System processes multiple UDP packets sequentially
- Network round-trip latency multiplied by number of packets
- Frame rate depends on UDP rate and frame size

For example:
- localhost with 9216 UDP limit: ~6.8 fps for 64×64
- Network server with latency: ~2.7 fps for 320×64

## References

- Canvas implementation: `flaschen_taschen/client/canvas.py`
- PPM formatter: `flaschen_taschen/client/ppm_formatter.py`
- Related: `PacketSize.md` (UDP limits and environment variables)
- Related: `PacketHandling.md` (server compatibility)
