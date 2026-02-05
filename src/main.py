#!/usr/bin/env python3
"""
Wallpaper Changer - 主程序入口
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("Wallpaper Changer")
    app.setOrganizationName("PanCodeInventory")

    # 启用高DPI缩放
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # 创建主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
