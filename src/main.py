#!/usr/bin/env python3
"""
Wallpaper Changer - Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add current directory to sys.path (fixes import issues in PyInstaller)
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# If running from PyInstaller bundle, also add MEIPASS to path
if getattr(sys, 'frozen', False):
    sys.path.insert(0, sys._MEIPASS)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.main_window import MainWindow


def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setApplicationName("Wallpaper Changer")
    app.setOrganizationName("PanCodeInventory")

    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
