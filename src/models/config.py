"""
配置管理
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class Config:
    """配置管理器"""

    DEFAULT_CONFIG = {
        "update_frequency": "daily",
        "update_time": "12:00",
        "interval_hours": 1,
        "resolution": {
            "mode": "auto",
            "custom_width": 1920,
            "custom_height": 1080,
            "prefer_higher": True
        },
        "sources": ["unsplash"],
        "categories": ["nature", "architecture", "minimal"],
        "api_keys": {
            "unsplash": "",
            "wallhaven": ""
        },
        "cache": {
            "enabled": True,
            "max_size_mb": 500,
            "max_images": 50
        },
        "wallpaper_mode": "fill",
        "auto_start": True
    }

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有字段存在
                return self._merge_config(self.DEFAULT_CONFIG, config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()

    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并配置（递归）"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def save(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"Config saved to: {self.config_path}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save()

    def get_update_frequency(self) -> str:
        """获取更新频率"""
        return self.get('update_frequency', 'daily')

    def get_update_time(self) -> str:
        """获取更新时间"""
        return self.get('update_time', '12:00')

    def get_interval_hours(self) -> int:
        """获取间隔小时数"""
        return self.get('interval_hours', 1)

    def get_resolution_mode(self) -> str:
        """获取分辨率模式"""
        return self.get('resolution.mode', 'auto')

    def get_custom_resolution(self) -> tuple:
        """获取自定义分辨率"""
        return (
            self.get('resolution.custom_width', 1920),
            self.get('resolution.custom_height', 1080)
        )

    def prefer_higher_resolution(self) -> bool:
        """是否偏好更高分辨率"""
        return self.get('resolution.prefer_higher', True)

    def get_sources(self) -> List[str]:
        """获取壁纸源"""
        return self.get('sources', ['unsplash'])

    def get_categories(self) -> List[str]:
        """获取分类"""
        return self.get('categories', ['nature', 'architecture'])

    def get_api_key(self, source: str) -> str:
        """获取 API 密钥"""
        return self.get(f'api_keys.{source}', '')

    def set_api_key(self, source: str, key: str):
        """设置 API 密钥"""
        self.set(f'api_keys.{source}', key)

    def get_cache_max_size(self) -> int:
        """获取缓存最大大小（MB）"""
        return self.get('cache.max_size_mb', 500)

    def get_cache_max_images(self) -> int:
        """获取缓存最大图片数"""
        return self.get('cache.max_images', 50)

    def get_wallpaper_mode(self) -> str:
        """获取壁纸显示模式"""
        return self.get('wallpaper_mode', 'fill')

    def is_auto_start(self) -> bool:
        """是否开机自启动"""
        return self.get('auto_start', True)
