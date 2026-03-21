# PyPI Release Guide

Instructions for preparing and publishing releases to PyPI.

## Prerequisites

- PyPI account created at https://pypi.org
- API token generated and stored in `~/.pypirc`
- `twine` installed: `pip install twine`
- `build` installed: `pip install build`

## Setup (One-Time)

### Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create account and verify email

### Generate API Token

1. Log in at https://pypi.org
2. Click username → Account settings
3. Find "API tokens" on the left
4. Click "Add API token"
5. Name: "release-token"
6. Scope: "Entire account"
7. Copy token immediately (only shown once)

### Configure `~/.pypirc`

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your token here
EOF

chmod 600 ~/.pypirc
```

## Release Workflow

### 1. Update Version Number

Update in both files (must match):

**pyproject.toml:**
```toml
[project]
name = "flaschen-taschen-py"
version = "0.1.2"  # Bump here
```

**setup.py:**
```python
setup(
    name="flaschen-taschen-py",
    version="0.1.2",  # Bump here
```

### 2. Update Documentation

Update `docs/` if needed:
- API changes → update `docs/api/*.md`
- New features → update `docs/guides/*.md`
- New examples → add to `docs/examples/cookbook.md`

### 3. Commit Changes

```bash
git add pyproject.toml setup.py docs/
git commit -m "version 0.1.2: description of changes"
git tag v0.1.2
git push origin main
git push origin main --tags
```

### 4. Build Distribution

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
python -m build
```

Expected output:
```
Successfully built flaschen_taschen_py-0.1.2.tar.gz and flaschen_taschen_py-0.1.2-py3-none-any.whl
```

### 5. Validate Package

```bash
twine check dist/*
```

Should output:
```
Checking dist/flaschen_taschen_py-0.1.2-py3-none-any.whl: PASSED
Checking dist/flaschen_taschen_py-0.1.2.tar.gz: PASSED
```

### 6. Upload to PyPI

```bash
twine upload dist/*
```

Expected output:
```
View at:
https://pypi.org/project/flaschen-taschen-py/0.1.2/
```

### 7. Verify on PyPI

Visit: `https://pypi.org/project/flaschen-taschen-py/`

Check:
- Latest version is correct
- README displays properly
- Documentation link works

### 8. Test Installation

```bash
pip install --force-reinstall flaschen-taschen-py
python -c "import flaschen_taschen; print('✓ Installed successfully')"
```

## Versioning Strategy

Use **Semantic Versioning**: MAJOR.MINOR.PATCH

| Type | Example | When |
|------|---------|------|
| Patch | 0.1.1 → 0.1.2 | Bug fixes, small improvements |
| Minor | 0.1.0 → 0.2.0 | New features (backward compatible) |
| Major | 0.1.0 → 1.0.0 | Breaking changes, major rewrite |

Current version: **0.1.1** (Pre-release, API may change)

## Common Issues

### Error: "400 Bad Request - File already exists"

**Cause:** Trying to upload a version that already exists on PyPI (same file hash)

**Solution:** Bump version number and rebuild
```bash
# Update version in pyproject.toml and setup.py
# Then:
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```

### Error: "403 Forbidden - Invalid authentication"

**Cause:** Invalid or expired API token in `~/.pypirc`

**Solution:** Generate new token
```bash
# Go to https://pypi.org/account/ → API tokens
# Create new token and update ~/.pypirc
```

### Error: "twine: command not found"

**Solution:** Install twine
```bash
pip install twine
```

### Files not included in wheel

**Cause:** Subpackage missing from `pyproject.toml [tool.setuptools] packages`

**Solution:** Ensure all subpackages are listed:
```toml
[tool.setuptools]
packages = [
    "flaschen_taschen",
    "flaschen_taschen.client",
    "flaschen_taschen.demos",
    "flaschen_taschen.generators",
    "flaschen_taschen.utils",
    "flaschen_taschen.cli",
]
```

## Troubleshooting

### Check what's on PyPI

```bash
pip index versions flaschen-taschen-py
```

### List local wheel contents

```bash
python -m zipfile -l dist/*.whl
```

### Test with local wheel before uploading

```bash
pip install --force-reinstall dist/*.whl
python -m flaschen_taschen.demos.plasma -t 5
send-text "Test"
```

## Quick Reference

```bash
# Full release workflow (one-liner)
nano pyproject.toml setup.py  # Update versions
git add pyproject.toml setup.py && git commit -m "version X.Y.Z" && git tag vX.Y.Z && git push origin main --tags
rm -rf dist/ build/ *.egg-info && python -m build
twine check dist/*
twine upload dist/*

# After upload, verify
pip index versions flaschen-taschen-py
```

## GitHub Releases (Optional)

Create a release on GitHub after uploading to PyPI:

```bash
gh release create v0.1.2 dist/* \
  --title "Version 0.1.2" \
  --notes "Changelog here"
```

Or via GitHub UI: https://github.com/FlaschenTaschen/ft-py/releases

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
