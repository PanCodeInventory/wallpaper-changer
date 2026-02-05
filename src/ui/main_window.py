"""
主窗口
"""

import sys
import random
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction,
                             QStatusBar, QMessageBox, QInputDialog, QComboBox,
                             QSpinBox, QDateTimeEdit, QCheckBox, QGroupBox,
                             QFormLayout, QLineEdit, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

from models.config import Config
from core.wallpaper_api import UnsplashAPI, WallhavenAPI
from core.wallpaper_downloader import WallpaperDownloader
from core.wallpaper_setter import WallpaperSetter, WallpaperStyle
from core.scheduler import WallpaperScheduler
from utils.screen_info import ScreenInfo


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("设置")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # 更新频率
        freq_group = QGroupBox("更新频率")
        freq_layout = QFormLayout()

        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["daily", "hourly"])
        self.freq_combo.setCurrentText(self.config.get_update_frequency())
        freq_layout.addRow("频率:", self.freq_combo)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.fromString(self.config.get_update_time(), "HH:mm"))
        freq_layout.addRow("时间:", self.time_edit)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 24)
        self.interval_spin.setValue(self.config.get_interval_hours())
        freq_layout.addRow("间隔(小时):", self.interval_spin)

        freq_group.setLayout(freq_layout)
        layout.addWidget(freq_group)

        # 分辨率设置
        res_group = QGroupBox("分辨率")
        res_layout = QFormLayout()

        self.res_mode_combo = QComboBox()
        self.res_mode_combo.addItems(["auto", "custom"])
        self.res_mode_combo.setCurrentText(self.config.get_resolution_mode())
        res_layout.addRow("模式:", self.res_mode_combo)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 7680)
        width, height = self.config.get_custom_resolution()
        self.width_spin.setValue(width)
        res_layout.addRow("宽度:", self.width_spin)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 4320)
        self.height_spin.setValue(height)
        res_layout.addRow("高度:", self.height_spin)

        self.higher_check = QCheckBox("偏好更高分辨率")
        self.higher_check.setChecked(self.config.prefer_higher_resolution())
        res_layout.addRow(self.higher_check)

        res_group.setLayout(res_layout)
        layout.addWidget(res_group)

        # API 密钥
        api_group = QGroupBox("API 密钥")
        api_layout = QFormLayout()

        self.unsplash_key = QLineEdit()
        self.unsplash_key.setText(self.config.get_api_key('unsplash'))
        self.unsplash_key.setPlaceholderText("Unsplash Access Key")
        api_layout.addRow("Unsplash:", self.unsplash_key)

        self.wallhaven_key = QLineEdit()
        self.wallhaven_key.setText(self.config.get_api_key('wallhaven'))
        self.wallhaven_key.setPlaceholderText("Wallhaven API Key (可选)")
        api_layout.addRow("Wallhaven:", self.wallhaven_key)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        """获取设置"""
        return {
            'update_frequency': self.freq_combo.currentText(),
            'update_time': self.time_edit.time().toString("HH:mm"),
            'interval_hours': self.interval_spin.value(),
            'resolution_mode': self.res_mode_combo.currentText(),
            'custom_width': self.width_spin.value(),
            'custom_height': self.height_spin.value(),
            'prefer_higher': self.higher_check.isChecked(),
            'unsplash_key': self.unsplash_key.text(),
            'wallhaven_key': self.wallhaven_key.text()
        }


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.init_components()
        self.init_ui()
        self.init_tray()

    def init_components(self):
        """初始化组件"""
        # 配置
        self.config = Config()

        # 下载器
        cache_dir = Path(__file__).parent.parent.parent / "cache"
        self.downloader = WallpaperDownloader(
            cache_dir=str(cache_dir),
            max_size_mb=self.config.get_cache_max_size(),
            max_images=self.config.get_cache_max_images()
        )

        # API
        unsplash_key = self.config.get_api_key('unsplash')
        wallhaven_key = self.config.get_api_key('wallhaven')

        self.apis = {}

        if unsplash_key:
            self.apis['unsplash'] = UnsplashAPI(unsplash_key)

        if wallhaven_key:
            self.apis['wallhaven'] = WallhavenAPI(wallhaven_key)

        # 设置器
        self.setter = WallpaperSetter()

        # 调度器
        self.scheduler = WallpaperScheduler()
        self.scheduler.set_update_callback(self.change_wallpaper)

        # 配置调度
        freq = self.config.get_update_frequency()
        if freq == 'daily':
            self.scheduler.schedule_daily(self.config.get_update_time())
        else:
            self.scheduler.schedule_hourly(self.config.get_interval_hours())

        # 启动调度器
        self.scheduler.start()

        # 当前壁纸历史
        self.wallpaper_history = []

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
        self.preview_label = QLabel("壁纸预览")
        self.preview_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(400)
        self.preview_label.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #ccc;
            border-radius: 10px;
        """)
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.next_btn = QPushButton("下一张壁纸")
        self.prev_btn = QPushButton("上一张壁纸")
        self.settings_btn = QPushButton("设置")
        self.refresh_btn = QPushButton("刷新壁纸库")

        button_layout.addWidget(self.prev_btn)
        button_layout.addWidget(self.next_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.settings_btn)

        layout.addLayout(button_layout)

        # 信息区域
        info_label = QLabel(self._get_info_text())
        info_label.setStyleSheet("color: #666; font-size: 12px; margin-top: 10px;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("欢迎使用壁纸更换器！")

        # 连接信号
        self.next_btn.clicked.connect(self.on_next_wallpaper)
        self.prev_btn.clicked.connect(self.on_prev_wallpaper)
        self.settings_btn.clicked.connect(self.on_settings)
        self.refresh_btn.clicked.connect(self.on_refresh)

    def _get_info_text(self):
        """获取信息文本"""
        width, height = ScreenInfo.get_screen_resolution()
        cache_size = self.downloader.get_cache_size()
        next_run = self.scheduler.get_next_run_time()

        info = f"屏幕: {width}x{height} | 缓存: {cache_size}"
        if next_run:
            info += f" | 下次更新: {next_run.strftime('%H:%M')}"

        return info

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

        # 显示托盘图标
        self.tray_icon.show()

    def change_wallpaper(self):
        """更换壁纸"""
        if not self.apis:
            self.statusBar.showMessage("请先配置 API 密钥")
            return

        try:
            # 随机选择一个 API
            api_name = random.choice(list(self.apis.keys()))
            api = self.apis[api_name]

            # 获取分辨率
            width, height = ScreenInfo.recommend_resolution(
                mode=self.config.get_resolution_mode(),
                prefer_higher=self.config.prefer_higher_resolution()
            )

            # 获取分类
            categories = self.config.get_categories()
            category = random.choice(categories)

            # 获取图片
            self.statusBar.showMessage(f"正在从 {api_name} 获取壁纸...")

            if api_name == 'unsplash':
                images = api.fetch_random(query=category, count=1)
            else:
                images = api.fetch_random(count=1)

            if not images:
                self.statusBar.showMessage("获取壁纸失败")
                return

            image = images[0]

            # 下载
            local_path = self.downloader.download(image['url'], image)
            if not local_path:
                self.statusBar.showMessage("下载壁纸失败")
                return

            # 设置壁纸
            mode = self.config.get_wallpaper_mode()
            style = getattr(WallpaperStyle, mode.upper(), WallpaperStyle.FILL)

            if self.setter.set_wallpaper(str(local_path), style):
                # 添加到历史
                self.wallpaper_history.append(local_path)

                # 更新预览
                self._update_preview(local_path)

                self.statusBar.showMessage(f"壁纸已更新: {image['description']}")
            else:
                self.statusBar.showMessage("设置壁纸失败")

        except Exception as e:
            self.statusBar.showMessage(f"错误: {str(e)}")

    def _update_preview(self, image_path: str):
        """更新预览"""
        try:
            pixmap = QPixmap(str(image_path))
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Error updating preview: {e}")

    def on_next_wallpaper(self):
        """下一张壁纸"""
        self.change_wallpaper()

    def on_prev_wallpaper(self):
        """上一张壁纸"""
        if len(self.wallpaper_history) >= 2:
            # 切换到上一张
            current = self.wallpaper_history.pop()
            prev = self.wallpaper_history[-1]

            mode = self.config.get_wallpaper_mode()
            style = getattr(WallpaperStyle, mode.upper(), WallpaperStyle.FILL)

            if self.setter.set_wallpaper(str(prev), style):
                self._update_preview(prev)
                self.statusBar.showMessage("已切换到上一张壁纸")
            else:
                self.wallpaper_history.append(current)
                self.statusBar.showMessage("切换失败")
        else:
            self.statusBar.showMessage("没有历史壁纸")

    def on_settings(self):
        """打开设置"""
        dialog = SettingsDialog(self.config, self)
        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()

            # 保存配置
            self.config.set('update_frequency', settings['update_frequency'])
            self.config.set('update_time', settings['update_time'])
            self.config.set('interval_hours', settings['interval_hours'])
            self.config.set('resolution.mode', settings['resolution_mode'])
            self.config.set('resolution.custom_width', settings['custom_width'])
            self.config.set('resolution.custom_height', settings['custom_height'])
            self.config.set('resolution.prefer_higher', settings['prefer_higher'])
            self.config.set('api_keys.unsplash', settings['unsplash_key'])
            self.config.set('api_keys.wallhaven', settings['wallhaven_key'])

            # 重新初始化组件
            self.init_components()

            QMessageBox.information(self, "设置", "设置已保存，将在下次更新时生效")

    def on_refresh(self):
        """刷新壁纸库"""
        self.statusBar.showMessage("正在刷新壁纸库...")

        if not self.apis:
            self.statusBar.showMessage("请先配置 API 密钥")
            return

        try:
            # 预加载几张壁纸
            api_name = random.choice(list(self.apis.keys()))
            api = self.apis[api_name]

            categories = self.config.get_categories()
            category = random.choice(categories)

            self.statusBar.showMessage(f"正在从 {api_name} 下载壁纸...")

            if api_name == 'unsplash':
                images = api.fetch_random(query=category, count=5)
            else:
                images = api.fetch_random(count=5)

            if images:
                # 下载所有图片
                for image in images:
                    self.downloader.download(image['url'], image)

                self.statusBar.showMessage(f"已下载 {len(images)} 张壁纸")
            else:
                self.statusBar.showMessage("获取壁纸失败")

        except Exception as e:
            self.statusBar.showMessage(f"错误: {str(e)}")

    def closeEvent(self, event):
        """关闭事件"""
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.scheduler.stop()
            event.accept()


# 修复导入
from PyQt5.QtCore import QTime
