#!/usr/bin/env python3
"""
Wallpaper Changer - Main Entry Point
"""

import sys
import os
from pathlib import Path

# PyInstaller hack: Get the temp folder where the bundle is unpacked
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
    src_dir = bundle_dir / 'src'
else:
    # Running in normal Python environment
    src_dir = Path(__file__).parent

# Add src directory to Python path
sys.path.insert(0, str(src_dir))

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
