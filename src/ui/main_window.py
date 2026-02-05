"""
主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction,
                             QStatusBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_tray()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Wallpaper Changer")
        self.setMinimumSize(800, 600)

        # 中心窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel("自动壁纸更换器")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 壁纸预览区域
        preview_label = QLabel("壁纸预览")
        preview_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(preview_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.next_btn = QPushButton("下一张壁纸")
        self.prev_btn = QPushButton("上一张壁纸")
        self.settings_btn = QPushButton("设置")

        button_layout.addWidget(self.prev_btn)
        button_layout.addWidget(self.next_btn)
        button_layout.addWidget(self.settings_btn)

        layout.addLayout(button_layout)

        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("欢迎使用壁纸更换器！")

        # 连接信号
        self.next_btn.clicked.connect(self.on_next_wallpaper)
        self.prev_btn.clicked.connect(self.on_prev_wallpaper)
        self.settings_btn.clicked.connect(self.on_settings)

    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)

        # 创建托盘菜单
        tray_menu = QMenu()

        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        next_action = QAction("下一张壁纸", self)
        next_action.triggered.connect(self.on_next_wallpaper)
        tray_menu.addAction(next_action)

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # 设置托盘图标（需要添加图标文件）
        # self.tray_icon.setIcon(QIcon("resources/icons/tray.ico"))

        # 显示托盘图标
        self.tray_icon.show()

    def on_next_wallpaper(self):
        """下一张壁纸"""
        self.statusBar.showMessage("正在更换壁纸...")
        # TODO: 实现壁纸更换逻辑
        QTimer.singleShot(1000, lambda: self.statusBar.showMessage("壁纸已更换！"))

    def on_prev_wallpaper(self):
        """上一张壁纸"""
        self.statusBar.showMessage("切换到上一张壁纸...")
        # TODO: 实现上一张壁纸逻辑
        QTimer.singleShot(1000, lambda: self.statusBar.showMessage("已切换！"))

    def on_settings(self):
        """打开设置"""
        self.statusBar.showMessage("打开设置...")
        # TODO: 实现设置对话框
        pass

    def closeEvent(self, event):
        """关闭事件"""
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
