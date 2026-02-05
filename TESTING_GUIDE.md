# Local Testing Guide

## Goal

Test the Wallpaper Changer application locally on Windows before creating a release. This prevents repeated build-test-fix cycles.

## Prerequisites

1. Windows 10 or later
2. Python 3.8+ installed
3. Git installed

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PanCodeInventory/wallpaper-changer.git
cd wallpaper-changer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Basic Import Tests

```bash
cd wallpaper-changer
python test.py
```

Expected output:
```
[START] Testing core functionality
=================================================
Testing Module Imports
=================================================
[OK] PyQt5
[OK] Config
[OK] ScreenInfo
[OK] WallpaperAPI
[OK] WallpaperDownloader
[OK] WallpaperSetter
[OK] Scheduler

All modules imported successfully!

=================================================
Testing Configuration
=================================================
Update frequency: daily
Update time: 12:00
Resolution mode: auto
Sources: ['unsplash', 'wallhaven']
Cache max size: 500 MB
[OK] Config test passed

=================================================
Testing Screen Info
=================================================
Screen resolution: 1920x1080
DPI: 96
Scale factor: 1.0
Formatted: 1920x1080 (FHD)
[OK] ScreenInfo test passed

=================================================
Testing Downloader
=================================================
Cache directory: /path/to/cache
Cache size: 0.00 MB
Cached wallpapers: 0
[OK] Downloader test passed

=================================================
[SUCCESS] All tests passed!
=================================================
```

### 4. Run the Application

```bash
python src/main.py
```

Expected result:
- Window opens successfully
- No import errors
- UI displays correctly

### 5. Test Core Functionality

#### A. Test Settings Dialog

1. Click "Settings" button
2. Verify dialog opens
3. Enter test API key (any string)
4. Click OK
5. Verify settings are saved to config.json

#### B. Test Wallpaper Download (without API)

1. Check if you have an Unsplash Access Key
   - If yes, enter it in Settings
   - If no, skip this test for now

#### C. Test Window Behavior

1. Minimize window - should minimize to tray
2. Close window - should hide to tray
3. Right-click tray icon - should show menu
4. Click "Show Window" - should show window again
5. Click "Exit" - should close application

### 6. Test PyInstaller Build Locally

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name=WallpaperChanger --clean --noconfirm --paths src --hidden-import platform --hidden-import sys --hidden-import os --hidden-import json --hidden-import random --hidden-import hashlib --hidden-import time --hidden-import ctypes src/main.py

# Test the built executable
dist\WallpaperChanger.exe
```

Expected result:
- exe file is created in `dist/` folder
- exe file size should be > 10 MB
- exe runs without import errors

## Testing Checklist

Before confirming "Tests Passed", verify:

- [ ] All import tests pass (test.py)
- [ ] Application opens successfully (python src/main.py)
- [ ] Settings dialog opens and saves config
- [ ] Window minimizes/maximizes correctly
- [ ] System tray icon appears and menu works
- [ ] PyInstaller build creates exe
- [ ] Built exe runs without import errors
- [ ] No ModuleNotFoundError errors
- [ ] No Unicode/encoding errors

## If Tests Fail

### Common Issues and Solutions

#### Issue: ModuleNotFoundError

**Symptom:**
```
ModuleNotFoundError: No module named 'ui'
```

**Solution:**
This should be fixed in current code. Verify you're running from the repository root directory.

#### Issue: PyQt5 not found

**Symptom:**
```
ModuleNotFoundError: No module named 'PyQt5'
```

**Solution:**
```bash
pip install PyQt5
```

#### Issue: platform not found

**Symptom:**
```
ModuleNotFoundError: No module named 'platform'
```

**Solution:**
This should be fixed with --hidden-import platform in PyInstaller. If still fails:
```bash
pyinstaller --onefile --windowed --name=WallpaperChanger --hidden-import platform src/main.py
```

#### Issue: Cannot access Windows API

**Symptom:**
Application crashes or wallpaper doesn't change

**Solution:**
- Verify you're running on Windows
- Check that pywin32 is installed:
  ```bash
  pip install pywin32
  ```
- Run as administrator if needed

## Reporting Test Results

After testing, report:

1. **Status:** PASS / FAIL
2. **Python Version:** `python --version`
3. **OS:** Windows version
4. **Test Results:**
   - Import tests: PASS/FAIL
   - App launch: PASS/FAIL
   - Settings dialog: PASS/FAIL
   - PyInstaller build: PASS/FAIL
   - Built exe runs: PASS/FAIL
5. **Errors (if any):** Full error messages

## When to Create Release

Only create a new release after:

1. ✅ All local tests pass
2. ✅ Application runs without import errors
3. ✅ PyInstaller builds successfully
4. ✅ Built exe runs correctly
5. ✅ No ModuleNotFoundError errors

## Quick Commands Summary

```bash
# Clone and setup
git clone https://github.com/PanCodeInventory/wallpaper-changer.git
cd wallpaper-changer
pip install -r requirements.txt

# Run tests
python test.py

# Run app
python src/main.py

# Build exe
pyinstaller --onefile --windowed --name=WallpaperChanger --clean --noconfirm --paths src --hidden-import platform --hidden-import sys --hidden-import os --hidden-import json --hidden-import random --hidden-import hashlib --hidden-import time --hidden-import ctypes src/main.py

# Test exe
dist\WallpaperChanger.exe
```

## Benefits of This Approach

1. **Faster iteration:** No waiting for CI builds
2. **Immediate feedback:** See errors right away
3. **Save resources:** Fewer CI build minutes
4. **More reliable:** Actual Windows testing, not CI emulation
5. **Better quality:** Thorough testing before release

## Next Steps After Passing Tests

1. Commit any final fixes if needed
2. Create a new version tag
3. Push to GitHub
4. Let CI build and release
5. Download and verify the release

This should result in a working, tested release on first try!
