# Wallpaper Changer

自动壁纸更换器 - Windows 桌面壁纸定时更换工具

## 功能特性

- ✅ 自动从 Unsplash、Wallhaven 等网站下载高清壁纸
- ✅ 定时自动更换壁纸（每小时/每天/自定义）
- ✅ 智能分辨率匹配（自动/手动/更高分辨率）
- ✅ 壁纸缓存管理
- ✅ 美观的 PyQt5 界面
- ✅ 系统托盘图标
- ✅ 开机自启动

## 截图

![界面截图](screenshots/main-window.png)

## 下载安装

### 方式一：下载 exe（推荐）

从 [Releases](../../releases) 页面下载最新版本的 `WallpaperChanger.exe`

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/PanCodeInventory/wallpaper-changer.git
cd wallpaper-changer

# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py
```

## 使用说明

1. 首次运行后，在设置中配置更新频率和时间
2. 选择壁纸来源和分辨率偏好
3. 程序会自动在后台运行，按时更换壁纸
4. 可以手动点击"下一张"按钮立即更换

## 配置文件

配置文件位置：`config.json`

```json
{
  "update_frequency": "daily",
  "update_time": "12:00",
  "resolution": {
    "mode": "auto",
    "prefer_higher": true
  },
  "sources": ["unsplash", "wallhaven"],
  "cache": {
    "max_size_mb": 500,
    "max_images": 50
  }
}
```

## 技术栈

- Python 3.8+
- PyQt5 - GUI 框架
- requests - HTTP 请求
- Pillow - 图片处理
- pywin32 - Windows API 调用
- schedule - 定时任务

## 开发计划

- [ ] 多壁纸源支持（Unsplash, Wallhaven, Pexels）
- [ ] 智能分辨率匹配
- [ ] 壁纸历史记录
- [ ] 主题切换
- [ ] 批量下载壁纸

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

PanCodeInventory

## 致谢

- Unsplash - 免费高质量图片
- Wallhaven - 高清壁纸社区
- PyQt5 - 强大的 GUI 框架
