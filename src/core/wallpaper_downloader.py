"""
壁纸下载器
负责下载和缓存壁纸
"""

import os
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import urlparse


class WallpaperDownloader:
    """壁纸下载器"""

    def __init__(self, cache_dir: str = "cache", max_size_mb: int = 500,
                 max_images: int = 50):
        self.cache_dir = Path(cache_dir)
        self.max_size_mb = max_size_mb
        self.max_images = max_images

        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, url: str) -> Path:
        """
        根据URL生成缓存路径

        Args:
            url: 图片URL

        Returns:
            缓存文件路径
        """
        # 使用URL的哈希作为文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()
        ext = self._get_extension(url)
        return self.cache_dir / f"{url_hash}{ext}"

    def _get_extension(self, url: str) -> str:
        """从URL获取文件扩展名"""
        parsed = urlparse(url)
        path = parsed.path.lower()

        if path.endswith('.jpg') or path.endswith('.jpeg'):
            return '.jpg'
        elif path.endswith('.png'):
            return '.png'
        elif path.endswith('.webp'):
            return '.webp'
        else:
            # 默认使用 jpg
            return '.jpg'

    def download(self, url: str, info: Dict = None) -> Optional[Path]:
        """
        下载壁纸到缓存

        Args:
            url: 图片URL
            info: 图片信息元数据

        Returns:
            本地文件路径，失败返回 None
        """
        # 检查是否已缓存
        cache_path = self._get_cache_path(url)
        if cache_path.exists():
            print(f"Using cached: {cache_path}")
            return cache_path

        # 检查缓存大小限制
        if not self._check_cache_size():
            self._cleanup_cache()

        try:
            print(f"Downloading: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # 写入文件
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # 保存元数据
            if info:
                self._save_metadata(cache_path, info)

            print(f"Downloaded to: {cache_path}")
            return cache_path

        except Exception as e:
            print(f"Download error: {e}")
            # 删除不完整的文件
            if cache_path.exists():
                cache_path.unlink()
            return None

    def _save_metadata(self, image_path: Path, info: Dict):
        """保存图片元数据"""
        metadata_path = image_path.with_suffix('.json')
        import json
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

    def _load_metadata(self, image_path: Path) -> Optional[Dict]:
        """加载图片元数据"""
        metadata_path = image_path.with_suffix('.json')
        if not metadata_path.exists():
            return None

        import json
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def _check_cache_size(self) -> bool:
        """检查缓存是否在限制内"""
        files = list(self.cache_dir.glob('*.{jpg,png,jpeg,webp}'))

        if len(files) >= self.max_images:
            return False

        total_size = sum(f.stat().st_size for f in files)
        total_size_mb = total_size / (1024 * 1024)

        return total_size_mb <= self.max_size_mb

    def _cleanup_cache(self):
        """清理旧缓存文件"""
        files = list(self.cache_dir.glob('*.{jpg,png,jpeg,webp,json}'))

        if not files:
            return

        # 按修改时间排序
        files.sort(key=lambda f: f.stat().st_mtime)

        # 删除最旧的 20% 文件
        num_to_delete = max(1, len(files) // 5)
        for f in files[:num_to_delete]:
            f.unlink()
            print(f"Deleted old cache: {f}")

    def get_cached_wallpapers(self) -> list[Path]:
        """获取所有缓存的壁纸"""
        return list(self.cache_dir.glob('*.{jpg,png,jpeg,webp}'))

    def clear_cache(self):
        """清空缓存"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print("Cache cleared")

    def get_cache_size(self) -> str:
        """获取缓存大小"""
        files = list(self.cache_dir.glob('*.{jpg,png,jpeg,webp}'))
        total_size = sum(f.stat().st_size for f in files)
        total_size_mb = total_size / (1024 * 1024)
        return f"{total_size_mb:.2f} MB"
