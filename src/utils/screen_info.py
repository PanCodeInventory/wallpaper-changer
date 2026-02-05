"""
屏幕信息工具
"""

import ctypes
from typing import List, Tuple, Optional


class ScreenInfo:
    """屏幕信息获取器"""

    @staticmethod
    def get_screen_resolution() -> Tuple[int, int]:
        """
        获取主屏幕分辨率

        Returns:
            (宽度, 高度)
        """
        try:
            import tkinter as tk
            root = tk.Tk()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()
            return width, height
        except:
            # 默认返回 1920x1080
            return 1920, 1080

    @staticmethod
    def get_all_screens() -> List[Tuple[int, int]]:
        """
        获取所有屏幕分辨率

        Returns:
            屏幕分辨率列表 [(宽度, 高度), ...]
        """
        try:
            import tkinter as tk
            root = tk.Tk()

            screens = []
            num_screens = root.winfo_screens()

            for i in range(num_screens):
                # 注意：这里简化处理，实际可能需要更复杂的方法
                screens.append(root.winfo_screenwidth(), root.winfo_screenheight())

            root.destroy()
            return screens
        except:
            # 默认返回一个屏幕
            return [(1920, 1080)]

    @staticmethod
    def get_dpi() -> int:
        """
        获取 DPI 设置

        Returns:
            DPI 值
        """
        try:
            user32 = ctypes.windll.user32
            hdc = user32.GetDC(0)
            dpi = user32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            user32.ReleaseDC(0, hdc)
            return dpi
        except:
            return 96  # 默认 DPI

    @staticmethod
    def get_scale_factor() -> float:
        """
        获取缩放因子（用于高分屏）

        Returns:
            缩放因子（如 1.5 表示 150%）
        """
        dpi = ScreenInfo.get_dpi()
        return dpi / 96.0

    @staticmethod
    def recommend_resolution(mode: str = "auto",
                             prefer_higher: bool = True) -> Tuple[int, int]:
        """
        推荐分辨率

        Args:
            mode: auto/custom
            prefer_higher: 是否偏好更高分辨率

        Returns:
            (宽度, 高度)
        """
        width, height = ScreenInfo.get_screen_resolution()
        scale_factor = ScreenInfo.get_scale_factor()

        if mode == "auto":
            # 考虑 DPI 缩放
            if prefer_higher:
                # 推荐更高分辨率（至少 1.5 倍）
                width = int(width * max(1.5, scale_factor))
                height = int(height * max(1.5, scale_factor))
            else:
                # 推荐原始分辨率
                pass
        else:
            # 使用用户自定义分辨率
            pass

        return width, height

    @staticmethod
    def format_resolution(width: int, height: int) -> str:
        """格式化分辨率显示"""
        if width >= 3840:
            return f"{width}x{height} (4K)"
        elif width >= 2560:
            return f"{width}x{height} (2K/QHD)"
        elif width >= 1920:
            return f"{width}x{height} (FHD)"
        elif width >= 1280:
            return f"{width}x{height} (HD)"
        else:
            return f"{width}x{height}"


def get_screen_info() -> str:
    """
    获取屏幕信息字符串

    Returns:
        屏幕信息描述
    """
    width, height = ScreenInfo.get_screen_resolution()
    dpi = ScreenInfo.get_dpi()
    scale = ScreenInfo.get_scale_factor()
    formatted = ScreenInfo.format_resolution(width, height)

    return f"Resolution: {formatted} | DPI: {dpi} | Scale: {scale*100:.0f}%"
