"""
壁纸设置器
调用 Windows API 设置桌面壁纸
"""

import os
import ctypes
from pathlib import Path
from typing import Optional
from enum import Enum


class WallpaperStyle(Enum):
    """壁纸样式"""
    CENTER = 0        # 居中
    TILE = 1          # 平铺
    STRETCH = 2       # 拉伸
    KEEP_ASPECT = 3   # 保持比例
    CROP = 4          # 裁剪
    SPAN = 5          # 跨屏
    FILL = CROP       # 填充（与CROP相同）


class WallpaperSetter:
    """壁纸设置器 - Windows API"""

    def __init__(self):
        self.SPI_SETDESKWALLPAPER = 20
        self.SPIF_UPDATEINIFILE = 0x01
        self.SPIF_SENDWININICHANGE = 0x02
        self.SPIF_SENDCHANGE = 0x02

        # 加载系统库
        self.user32 = ctypes.windll.user32
        self.user32.SystemParametersInfoW.restype = ctypes.c_bool
        self.user32.SystemParametersInfoW.argtypes = [
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_wchar_p,
            ctypes.c_uint
        ]

    def set_wallpaper(self, image_path: str,
                      style: WallpaperStyle = WallpaperStyle.FILL) -> bool:
        """
        设置桌面壁纸

        Args:
            image_path: 图片路径（必须是绝对路径）
            style: 壁纸样式

        Returns:
            是否成功
        """
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return False

        # 转换为绝对路径
        image_path = os.path.abspath(image_path)

        # 设置壁纸样式
        self._set_style(style)

        try:
            # 调用 Windows API 设置壁纸
            result = self.user32.SystemParametersInfoW(
                self.SPI_SETDESKWALLPAPER,
                0,
                image_path,
                self.SPIF_UPDATEINIFILE | self.SPIF_SENDCHANGE
            )

            if result:
                print(f"Wallpaper set: {image_path}")
                return True
            else:
                print("Failed to set wallpaper")
                return False

        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            return False

    def _set_style(self, style: WallpaperStyle):
        """设置壁纸样式"""
        # Windows 壁纸样式注册表路径
        # HKEY_CURRENT_USER\Control Panel\Desktop\WallpaperStyle
        # HKEY_CURRENT_USER\Control Panel\Desktop\TileWallpaper

        import winreg

        try:
            # 打开注册表
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_SET_VALUE
            )

            # 设置样式值
            style_values = {
                WallpaperStyle.CENTER: ("0", "0"),
                WallpaperStyle.TILE: ("1", "1"),
                WallpaperStyle.STRETCH: ("2", "0"),
                WallpaperStyle.KEEP_ASPECT: ("6", "0"),
                WallpaperStyle.CROP: ("10", "0"),
                WallpaperStyle.SPAN: ("22", "0")
            }

            wallpaper_style, tile_wallpaper = style_values.get(
                style, ("2", "0")
            )

            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, wallpaper_style)
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, tile_wallpaper)

            winreg.CloseKey(key)

        except Exception as e:
            print(f"Error setting wallpaper style: {e}")

    def get_current_wallpaper(self) -> Optional[str]:
        """获取当前壁纸路径"""
        import winreg

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_READ
            )

            wallpaper, _ = winreg.QueryValueEx(key, "Wallpaper")
            winreg.CloseKey(key)

            return wallpaper

        except Exception as e:
            print(f"Error getting current wallpaper: {e}")
            return None

    def refresh_desktop(self):
        """刷新桌面"""
        # 发送 WM_SETTINGCHANGE 消息
        import ctypes
        from ctypes import wintypes

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_BLOCK = 0x0001

        def callback(result, lparam):
            pass

        self.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_BLOCK,
            5000,
            callback
        )


def set_wallpaper(image_path: str, style: str = "fill") -> bool:
    """
    便捷函数：设置壁纸

    Args:
        image_path: 图片路径
        style: 样式（center/tile/stretch/keep_aspect/crop/span/fill）

    Returns:
        是否成功
    """
    style_map = {
        "center": WallpaperStyle.CENTER,
        "tile": WallpaperStyle.TILE,
        "stretch": WallpaperStyle.STRETCH,
        "keep_aspect": WallpaperStyle.KEEP_ASPECT,
        "crop": WallpaperStyle.CROP,
        "span": WallpaperStyle.SPAN,
        "fill": WallpaperStyle.FILL
    }

    wallpaper_style = style_map.get(style.lower(), WallpaperStyle.FILL)

    setter = WallpaperSetter()
    return setter.set_wallpaper(image_path, wallpaper_style)
