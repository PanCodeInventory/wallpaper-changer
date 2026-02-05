#!/usr/bin/env python3
"""
简单的功能测试脚本
不依赖 tkinter，使用 PyQt5
"""

import sys
import platform

# 检查平台
if platform.system() != 'Windows':
    print("此应用仅支持 Windows 平台")
    sys.exit(1)

# 添加 src 目录到路径
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from models.config import Config
from utils.screen_info import ScreenInfo


def test_imports():
    """测试导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)

    try:
        print("✓ PyQt5")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt

        print("✓ Config")
        from models.config import Config

        print("✓ ScreenInfo")
        from utils.screen_info import ScreenInfo

        print("✓ WallpaperAPI")
        from core.wallpaper_api import UnsplashAPI, WallhavenAPI

        print("✓ WallpaperDownloader")
        from core.wallpaper_downloader import WallpaperDownloader

        print("✓ WallpaperSetter")
        from core.wallpaper_setter import WallpaperSetter, WallpaperStyle

        print("✓ Scheduler")
        from core.scheduler import WallpaperScheduler

        print("\n所有模块导入成功！\n")
        return True

    except Exception as e:
        print(f"\n导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """测试配置管理"""
    print("=" * 50)
    print("测试配置管理")
    print("=" * 50)

    try:
        config = Config()

        print(f"更新频率: {config.get_update_frequency()}")
        print(f"更新时间: {config.get_update_time()}")
        print(f"分辨率模式: {config.get_resolution_mode()}")
        print(f"壁纸源: {config.get_sources()}")
        print(f"缓存最大大小: {config.get_cache_max_size()} MB")

        print("✓ 配置管理测试通过\n")
        return True

    except Exception as e:
        print(f"✗ 配置管理测试失败: {e}\n")
        return False


def test_screen_info():
    """测试屏幕信息"""
    print("=" * 50)
    print("测试屏幕信息")
    print("=" * 50)

    try:
        # 需要创建 QApplication
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        width, height = ScreenInfo.get_screen_resolution()
        print(f"屏幕分辨率: {width}x{height}")

        dpi = ScreenInfo.get_dpi()
        print(f"DPI: {dpi}")

        scale = ScreenInfo.get_scale_factor()
        print(f"缩放因子: {scale}")

        formatted = ScreenInfo.format_resolution(width, height)
        print(f"格式化: {formatted}")

        print("✓ 屏幕信息测试通过\n")
        return True

    except Exception as e:
        print(f"✗ 屏幕信息测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_downloader():
    """测试下载器"""
    print("=" * 50)
    print("测试下载器")
    print("=" * 50)

    try:
        cache_dir = Path(__file__).parent / "cache"
        downloader = WallpaperDownloader(
            cache_dir=str(cache_dir),
            max_size_mb=500,
            max_images=50
        )

        print(f"缓存目录: {cache_dir}")
        print(f"缓存大小: {downloader.get_cache_size()}")
        print(f"缓存的壁纸数: {len(downloader.get_cached_wallpapers())}")

        print("✓ 下载器测试通过\n")
        return True

    except Exception as e:
        print(f"✗ 下载器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n🚀 开始测试核心功能\n")

    # 创建 QApplication（测试 GUI 需要）
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # 运行测试
    results = []

    results.append(test_imports())
    results.append(test_config())
    results.append(test_screen_info())
    results.append(test_downloader())

    print("=" * 50)
    if all(results):
        print("✅ 所有测试通过！")
        print("=" * 50)
    else:
        print("❌ 部分测试失败")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
