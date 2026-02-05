#!/usr/bin/env python3
"""
Simple functionality test script
No tkinter dependency, uses PyQt5
"""

import sys
import platform

# Check platform
if platform.system() != 'Windows':
    print("This application only supports Windows platform")
    sys.exit(1)

# Add src directory to path
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from models.config import Config
from utils.screen_info import ScreenInfo


def test_imports():
    """Test imports"""
    print("=" * 50)
    print("Testing Module Imports")
    print("=" * 50)

    try:
        print("[OK] PyQt5")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt

        print("[OK] Config")
        from models.config import Config

        print("[OK] ScreenInfo")
        from utils.screen_info import ScreenInfo

        print("[OK] WallpaperAPI")
        from core.wallpaper_api import UnsplashAPI, WallhavenAPI

        print("[OK] WallpaperDownloader")
        from core.wallpaper_downloader import WallpaperDownloader

        print("[OK] WallpaperSetter")
        from core.wallpaper_setter import WallpaperSetter, WallpaperStyle

        print("[OK] Scheduler")
        from core.scheduler import WallpaperScheduler

        print("\nAll modules imported successfully!\n")
        return True

    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration"""
    print("=" * 50)
    print("Testing Configuration")
    print("=" * 50)

    try:
        config = Config()

        print(f"Update frequency: {config.get_update_frequency()}")
        print(f"Update time: {config.get_update_time()}")
        print(f"Resolution mode: {config.get_resolution_mode()}")
        print(f"Sources: {config.get_sources()}")
        print(f"Cache max size: {config.get_cache_max_size()} MB")

        print("[OK] Config test passed\n")
        return True

    except Exception as e:
        print(f"[FAIL] Config test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_screen_info():
    """Test screen info"""
    print("=" * 50)
    print("Testing Screen Info")
    print("=" * 50)

    try:
        # Need to create QApplication
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        width, height = ScreenInfo.get_screen_resolution()
        print(f"Screen resolution: {width}x{height}")

        dpi = ScreenInfo.get_dpi()
        print(f"DPI: {dpi}")

        scale = ScreenInfo.get_scale_factor()
        print(f"Scale factor: {scale}")

        formatted = ScreenInfo.format_resolution(width, height)
        print(f"Formatted: {formatted}")

        print("[OK] ScreenInfo test passed\n")
        return True

    except Exception as e:
        print(f"[FAIL] ScreenInfo test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_downloader():
    """Test downloader"""
    print("=" * 50)
    print("Testing Downloader")
    print("=" * 50)

    try:
        cache_dir = Path(__file__).parent / "cache"
        downloader = WallpaperDownloader(
            cache_dir=str(cache_dir),
            max_size_mb=500,
            max_images=50
        )

        print(f"Cache directory: {cache_dir}")
        print(f"Cache size: {downloader.get_cache_size()}")
        print(f"Cached wallpapers: {len(downloader.get_cached_wallpapers())}")

        print("[OK] Downloader test passed\n")
        return True

    except Exception as e:
        print(f"[FAIL] Downloader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print("\n[START] Testing core functionality\n")

    # Create QApplication (needed for GUI tests)
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Run tests
    results = []

    results.append(test_imports())
    results.append(test_config())
    results.append(test_screen_info())
    results.append(test_downloader())

    print("=" * 50)
    if all(results):
        print("[SUCCESS] All tests passed!")
        print("=" * 50)
    else:
        print("[FAILED] Some tests failed")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
