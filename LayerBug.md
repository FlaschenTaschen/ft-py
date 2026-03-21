# Layer Bug Investigation - Summary

## Problem Statement
When running demos with `-l 5` (layer 5), the display server shows layer 0 instead. Example:
```bash
python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 5 boxes
# Display shows: Layers: 1  0 1,575px (should show layer 5)
```

## Root Causes Found and Fixed

### Fix #1: Layer Not Passed Through Stack (COMPLETE)

**Problem**: Layer argument parsed by StandardOptions but never reached the display server.

**Stack trace** (before fix):
1. User passes `-l 5` → StandardOptions parses correctly (std_opts.layer = 5)
2. Demo.setup() creates Config WITHOUT layer parameter (Config class had no layer support)
3. Canvas created with Config that has no layer
4. Canvas.send() calls `PPMFormatter.encode(..., layer=0,  # hardcoded)`
5. PPM metadata gets layer=0 → display shows layer 0

**Fixes Applied**:
- **flaschen_taschen/client/config.py**: Added `layer: int = 0` parameter to Config.__init__()
- **flaschen_taschen/demos/__init__.py** (Demo.setup(), line 57): Added `layer=self.std_opts.layer,` when creating Config
- **flaschen_taschen/client/canvas.py** (Canvas.send(), line 199): Changed from `layer=0,` to `layer=self.config.layer,`

**Verification**: All 151 tests pass. Layer correctly flows: CLI → StandardOptions → Config → Canvas → PPMFormatter

### Fix #2: PPM Header Format Was Incorrect (COMPLETE)

**Problem**: PPM metadata `#FT: x y z` was positioned BEFORE image dimensions, preventing display server from parsing it correctly.

**Wrong Format** (what Python was generating):
```
P6
#FT: 0 0 5          <- metadata BEFORE dimensions
45 35               <- dimensions AFTER metadata
255
```

**Correct Format** (C++ reference):
```
P6
45 35               <- dimensions first
#FT: 0 0 5          <- metadata after dimensions
255
```

**C++ Reference** (from flaschen-taschen/src/ft-display.cc):
```c
snprintf(header, sizeof(header), "P6\n%d %d\n#FT: %d %d %d\n255\n",
         width, send_h, off_x_, off_y_, off_z_);
```

**Fix Applied**:
- **flaschen_taschen/client/ppm_formatter.py** (encode method, lines 46-59):
  - Reordered header construction
  - FROM: magic + ft_metadata + dimensions + max_color
  - TO: magic + dimensions + ft_metadata + max_color

**Code Change**:
```python
# Correct order:
header = cls.PPM_MAGIC + b"\n"                              # P6\n
header += dimensions.encode("ascii")                        # 45 35\n
header += ft_metadata.encode("ascii")                       # #FT: 0 0 5\n
header += max_color.encode("ascii")                         # 255\n
```

**Verification**: PPM output now matches C++ format exactly. All 151 tests still pass.

## Current Status

### What's Working ✓
- StandardOptions correctly parses `-l 5` (verified with argparse behavior)
- Demo.setup() correctly passes layer to Config
- Canvas.send() correctly passes layer from config to PPMFormatter.encode()
- PPMFormatter.encode() correctly generates metadata `#FT: 0 0 5`
- PPM header format matches C++ reference exactly
- All 151 unit tests pass

### What's NOT Working ✗
- **Display server still shows layer 0** despite all of the above being correct
- Screenshot evidence: User ran `python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 5 boxes` and display showed "Layers: 1  0 1,575px"

## Possible Remaining Causes

### 1. Display Server Needs Restart
- Display server process may be caching old metadata parser state
- May need to kill/restart the server to recognize new PPM format

### 2. Display Server Metadata Parsing Bug
- Display server may have a bug in parsing `#FT:` metadata
- May ignore the metadata or parse it incorrectly
- Would require debugging the display server itself

### 3. Unknown Protocol Requirement
- There may be another step in the protocol for setting layer beyond PPM metadata
- Could be a separate UDP command, handshake, or initialization sequence
- Would need to inspect C++ client code or display server source

### 4. UDP Transmission Issue
- Metadata could be getting corrupted/lost during UDP transmission
- Packet fragmentation or truncation could strip the metadata line
- Would need UDP packet inspection/debugging

### 5. Display Server Configuration
- Layer feature may need to be enabled/configured on the display server
- Display server may have layer support disabled by default
- Would need to check display server startup options or configuration

## Test Cases Verified

```python
# Layer correctly flows through the entire stack:
std_opts = StandardOptions(['-l', '5', 'boxes'])
assert std_opts.layer == 5

config = Config(layer=std_opts.layer)
assert config.layer == 5

# PPM encodes layer in metadata:
ppm_data = PPMFormatter.encode(pixels, layer=5)
assert b"#FT: 0 0 5" in ppm_data  # layer=5 in metadata
```

## Next Steps to Debug

1. **Verify display server**: Check if server logs show it's parsing the `#FT:` metadata
2. **Inspect UDP packets**: Use tcpdump/Wireshark to verify metadata is being transmitted
3. **Restart display server**: Kill and restart the FT server process to clear any cached state
4. **Check server source**: Look at C++ display server code to see exactly how it parses metadata
5. **Test with C++ client**: Run a C++ demo with `-l 5` to verify layer works in C++ (confirms server supports it)

## Files Modified

1. `flaschen_taschen/client/config.py` - Added layer parameter
2. `flaschen_taschen/client/canvas.py` - Use config.layer instead of hardcoded 0
3. `flaschen_taschen/demos/__init__.py` - Pass layer from StandardOptions to Config
4. `flaschen_taschen/client/ppm_formatter.py` - Fixed PPM header format

## Verification Commands

```bash
# Verify PPM format (inspect binary data):
python3 -c "
from flaschen_taschen.client.ppm_formatter import PPMFormatter
pixels = [[(255, 0, 0) for _ in range(5)] for _ in range(5)]
ppm = PPMFormatter.encode(pixels, layer=5)
print(ppm[:100])  # Should show: P6\n5 5\n#FT: 0 0 5\n255\n
"

# Run test with explicit layer:
python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 1 boxes
# Check display - should show layer 5 (currently shows layer 0)
```
