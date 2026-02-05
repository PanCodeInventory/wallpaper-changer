"""
屏幕信息工具
使用 PyQt5 获取屏幕信息（避免 tkinter 依赖）
"""

import platform
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
            from PyQt5.QtWidgets import QApplication, QDesktopWidget

            # 创建 QApplication 实例（如果不存在）
            app = QApplication.instance()
            if app is None:
                app = QApplication([])

            screen = QDesktopWidget().screenGeometry()
            width = screen.width()
            height = screen.height()

            return width, height

        except Exception as e:
            print(f"Error getting screen resolution: {e}")
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
            from PyQt5.QtWidgets import QApplication, QDesktopWidget

            app = QApplication.instance()
            if app is None:
                app = QApplication([])

            desktop = QDesktopWidget()
            screen_count = desktop.screenCount()

            screens = []
            for i in range(screen_count):
                screen = desktop.screenGeometry(i)
                screens.append((screen.width(), screen.height()))

            return screens

        except Exception as e:
            print(f"Error getting all screens: {e}")
            # 默认返回一个屏幕
            return [(1920, 1080)]

    @staticmethod
    def get_dpi() -> int:
        """
        获取 DPI 设置

        Returns:
            DPI 值
        """
        if platform.system() == 'Windows':
            try:
                import ctypes
                user32 = ctypes.windll.user32
                hdc = user32.GetDC(0)
                dpi = user32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
                user32.ReleaseDC(0, hdc)
                return dpi
            except:
                return 96  # 默认 DPI
        else:
            return 96  # 非 Windows 平台默认 DPI

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
        elif mode == "custom":
            # 使用用户自定义分辨率（从配置读取）
            pass

        # 返回计算后的值
        return (width, height)

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
