# Layer Bug Investigation - RESOLVED ✓

## Problem Statement
When running demos with `-l 5` (layer 5), the display server shows layer 0 instead. Example:
```bash
python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 5 boxes
# Display shows: Layers: 1  0 1,575px (should show layer 5)
```

## Root Causes Found and Fixed

### Fix #1: Layer Not Passed Through Stack ✓

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

### Fix #2: PPM Format - Header vs Footer ✓

**Problem**: Initial implementation tried to use `#FT: x y z` format but placed it incorrectly. The official protocol supports TWO valid approaches (see `flaschen-taschen/doc/protocols.md`):

**Option 1: Header Format** (with `#FT:` comment):
```
P6
10 10
#FT: 5 8 13    ← #FT: in header as a PPM comment
255
[pixel data]
```

**Option 2: Footer Format** (raw values only, no prefix):
```
P6
10 10
255
[pixel data]
5              ← Just raw values, no #FT: prefix
8
13
```

**What we were generating (wrong)**:
- Tried to use `#FT: 0 0 5` in footer (mixing formats - `#FT:` is for header)

**What we fixed to (correct)**:
- Using Option 2: Footer format with raw values only: `\n0 0 5\n`
- This matches the Swift/C++ implementation exactly

**Swift Reference** (uses footer format):
```swift
let offsetString = String(format: "\n%d %d %d\n", x, y, z)
// Produces: \n0 0 5\n (just raw values, no prefix)
```

**Why Footer Format**: The docs note that footer format "is sometimes easier to do depending on your implementation" and makes it "backward compatible with standard PPM (as PPM just ignores additional data at the end)."

**Fix Applied**:
- **flaschen_taschen/client/ppm_formatter.py** (encode method):
  - Changed footer from: `f"#FT: {x_offset} {y_offset} {layer}\n"`
  - To: `f"\n{x_offset} {y_offset} {layer}\n"`
  - Moved metadata to footer (after pixel data), not header

- **flaschen_taschen/client/ppm_formatter.py** (decode method):
  - Updated to parse any line with three space-separated integers
  - Ignores lines starting with `#` (comments)

**Code Changes in `ppm_formatter.py`**:

*encode() method:*
```python
# OLD (mixing formats - #FT: belongs in header, not footer):
ft_metadata = f"#FT: {x_offset} {y_offset} {layer}\n"

# NEW (pure footer format with raw values):
ft_metadata = f"\n{x_offset} {y_offset} {layer}\n"
footer = ft_metadata.encode("ascii")
return header + pixel_data + footer
```

*decode() method:*
```python
# OLD: Looked for #FT: prefix
if "#FT:" in footer:
    ft_line = [line for line in footer.split("\n") if line.startswith("#FT:")][0]

# NEW: Look for any line with three space-separated integers (ignoring comments)
for line in footer.split("\n"):
    line = line.strip()
    if line and not line.startswith("#"):
        parts = line.split()
        if len(parts) >= 3:
            ft_data = {
                "x_offset": int(parts[0]),
                "y_offset": int(parts[1]),
                "layer": int(parts[2]),
            }
            break
```

**Verification**: PPM output now matches Swift/C++ format exactly. All 151 tests pass.

## Protocol Conformance

Per `flaschen-taschen/doc/protocols.md`:
- Both header format (`#FT: x y z`) and footer format (raw values) are valid
- **Implementation choice**: Python uses footer format (Option 2)
- **Rationale**: Simpler to implement, backward-compatible with standard PPM
- **Result**: Matches Swift/C++ behavior exactly

## Final Status

### ✓ RESOLVED
- Layer now correctly displays on the specified layer (e.g., `-l 5` shows layer 5)
- All 151 tests pass
- Format matches Swift and C++ implementations exactly
- Fully conforms to official FlaschenTaschen protocol specification

### Files Modified

1. `flaschen_taschen/client/config.py` - Added layer parameter
2. `flaschen_taschen/client/canvas.py` - Use config.layer instead of hardcoded 0
3. `flaschen_taschen/demos/__init__.py` - Pass layer from StandardOptions to Config
4. `flaschen_taschen/client/ppm_formatter.py` - Fixed footer format (removed `#FT:` prefix, use raw values)
5. `tests/test_ppm_formatter.py` - Updated tests to verify correct footer format

## Verification

```bash
# Layer now correctly flows through the entire stack and displays on the right layer
python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 5 boxes
# Display now shows: Layers: 1  5 (correct!)
```
