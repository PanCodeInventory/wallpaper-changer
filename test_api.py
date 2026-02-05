#!/usr/bin/env python3
"""
测试脚本 - 验证核心功能
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from models.config import Config
from core.wallpaper_api import UnsplashAPI
from core.wallpaper_downloader import WallpaperDownloader
from core.wallpaper_setter import WallpaperSetter
from utils.screen_info import ScreenInfo


def test_config():
    """测试配置管理"""
    print("=" * 50)
    print("测试配置管理")
    print("=" * 50)

    config = Config()

    print(f"更新频率: {config.get_update_frequency()}")
    print(f"更新时间: {config.get_update_time()}")
    print(f"分辨率模式: {config.get_resolution_mode()}")
    print(f"壁纸源: {config.get_sources()}")
    print(f"缓存最大大小: {config.get_cache_max_size()} MB")

    print("✓ 配置管理测试通过\n")


def test_screen_info():
    """测试屏幕信息"""
    print("=" * 50)
    print("测试屏幕信息")
    print("=" * 50)

    width, height = ScreenInfo.get_screen_resolution()
    print(f"屏幕分辨率: {width}x{height}")

    dpi = ScreenInfo.get_dpi()
    print(f"DPI: {dpi}")

    scale = ScreenInfo.get_scale_factor()
    print(f"缩放因子: {scale}")

    formatted = ScreenInfo.format_resolution(width, height)
    print(f"格式化: {formatted}")

    print("✓ 屏幕信息测试通过\n")


def test_unsplash_api():
    """测试 Unsplash API"""
    print("=" * 50)
    print("测试 Unsplash API")
    print("=" * 50)

    config = Config()
    api_key = config.get_api_key('unsplash')

    if not api_key:
        print("⚠ 未配置 Unsplash API 密钥，跳过测试\n")
        return

    api = UnsplashAPI(api_key)

    try:
        images = api.fetch_random(query="nature", count=2)
        print(f"获取到 {len(images)} 张图片")

        for img in images:
            print(f"  - ID: {img['id']}")
            print(f"    URL: {img['url']}")
            print(f"    分辨率: {img['width']}x{img['height']}")
            print(f"    描述: {img['description']}")

        print("✓ Unsplash API 测试通过\n")
    except Exception as e:
        print(f"✗ Unsplash API 测试失败: {e}\n")


def test_downloader():
    """测试下载器"""
    print("=" * 50)
    print("测试下载器")
    print("=" * 50)

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


def test_wallpaper_setter():
    """测试壁纸设置器"""
    print("=" * 50)
    print("测试壁纸设置器")
    print("=" * 50)

    setter = WallpaperSetter()

    current = setter.get_current_wallpaper()
    print(f"当前壁纸: {current}")

    print("✓ 壁纸设置器测试通过")
    print("  (未实际设置壁纸，仅检查 API 可用性)\n")


def main():
    """主函数"""
    print("\n🚀 开始测试核心功能\n")

    try:
        test_config()
        test_screen_info()
        test_unsplash_api()
        test_downloader()
        test_wallpaper_setter()

        print("=" * 50)
        print("✅ 所有测试完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
