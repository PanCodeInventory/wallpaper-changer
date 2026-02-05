"""
壁纸 API 集成
支持 Unsplash 和 Wallhaven
按照 Unsplash API 规范正确获取高分辨率图片
"""

import requests
import random
from typing import List, Dict, Optional
from pathlib import Path


class WallpaperAPI:
    """壁纸 API 基类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WallpaperChanger/1.0'
        })


class UnsplashAPI(WallpaperAPI):
    """Unsplash API - 按照官方规范获取高分辨率图片"""

    def __init__(self, access_key: str):
        super().__init__()
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com"
        self.session.headers.update({
            'Authorization': f'Client-ID {access_key}'
        })

    def _build_resolution_url(self, image: Dict, width: int, height: int, prefer_higher: bool = True) -> str:
        """
        根据 Unsplash 规范构建高分辨率 URL

        Unsplash API 文档：
        - 使用 raw URL 作为基础（只有 ixid 参数）
        - 添加动态参数：w, h, dpr, q, fit

        参数说明：
        - w: 宽度（像素）
        - h: 高度（像素）
        - dpr: 设备像素比（1, 2, 3 等）
        - q: 质量压缩（1-100，越高越好）
        - fit: 适应方式（max=适应，crop=裁剪，clip=裁剪扩展）
        - fm: 格式（jpg, png, webp）

        Args:
            image: Unsplash API 返回的图片对象
            width: 目标宽度
            height: 目标高度
            prefer_higher: 是否偏好更高分辨率（使用 DPR=2）

        Returns:
            高分辨率图片 URL
        """
        # 获取 raw URL 作为基础
        raw_url = image['urls']['raw']

        # 构建查询参数
        params = []

        # 添加宽度和高度
        params.append(f"w={width}")
        params.append(f"h={height}")

        # 添加 DPR（设备像素比），支持高分屏
        if prefer_higher:
            dpr = 2  # 2 倍分辨率，适合高分屏
        else:
            dpr = 1
        params.append(f"dpr={dpr}")

        # 添加质量参数（越高越好，但文件越大）
        params.append("q=95")

        # 添加适应方式（max=适应，不裁剪）
        params.append("fit=max")

        # 添加格式（使用 jpg）
        params.append("fm=jpg")

        # 组合 URL
        separator = '&' if '?' in raw_url else '?'
        high_res_url = f"{raw_url}{separator}{'&'.join(params)}"

        return high_res_url

    def fetch_random(self, query: str = None, count: int = 10,
                     orientation: str = 'landscape') -> List[Dict]:
        """
        获取随机图片

        Args:
            query: 搜索关键词
            count: 返回数量
            orientation: 方向（landscape/portrait/squarish）

        Returns:
            图片信息列表
        """
        params = {
            'count': count,
            'orientation': orientation,
            'featured': True
        }
        if query:
            params['query'] = query

        try:
            response = self.session.get(
                f"{self.base_url}/photos/random",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            images = response.json()

            return [{
                'id': img['id'],
                # 使用 full URL（最大尺寸）
                'url': img['urls']['full'],
                'full_url': img['urls']['full'],
                'download_url': img['links']['download'],
                'raw_url': img['urls']['raw'],  # 保存 raw URL 用于构建自定义分辨率
                'author': img['user']['name'],
                'description': img.get('description') or img.get('alt_description', ''),
                'width': img['width'],
                'height': img['height'],
                'source': 'unsplash'
            } for img in images]

        except Exception as e:
            print(f"Unsplash API error: {e}")
            return []

    def search(self, query: str, count: int = 10,
               orientation: str = 'landscape') -> List[Dict]:
        """
        搜索图片

        Args:
            query: 搜索关键词
            count: 返回数量
            orientation: 方向

        Returns:
            图片信息列表
        """
        params = {
            'query': query,
            'per_page': count,
            'orientation': orientation,
            'order_by': 'relevant'
        }

        try:
            response = self.session.get(
                f"{self.base_url}/search/photos",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            results = response.json()['results']

            return [{
                'id': img['id'],
                'url': img['urls']['full'],
                'full_url': img['urls']['full'],
                'download_url': img['links']['download'],
                'raw_url': img['urls']['raw'],
                'author': img['user']['name'],
                'description': img.get('description') or img.get('alt_description', ''),
                'width': img['width'],
                'height': img['height'],
                'source': 'unsplash'
            } for img in results]

        except Exception as e:
            print(f"Unsplash search error: {e}")
            return []

    def get_high_resolution_url(self, image: Dict, target_width: int, target_height: int,
                                prefer_higher: bool = True) -> str:
        """
        根据用户配置获取高分辨率图片 URL

        这是 Unsplash API 推荐的做法 - 使用动态参数而不是固定的尺寸 URL

        Args:
            image: Unsplash API 返回的图片对象
            target_width: 目标屏幕宽度
            target_height: 目标屏幕高度
            prefer_higher: 是否使用 DPR=2（推荐用于高分屏）

        Returns:
            高分辨率图片 URL
        """
        return self._build_resolution_url(
            image,
            target_width,
            target_height,
            prefer_higher
        )


class WallhavenAPI(WallpaperAPI):
    """Wallhaven API"""

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://wallhaven.cc/api/v1"

        if api_key:
            self.session.headers.update({
                'X-API-Key': api_key
            })

    def fetch_random(self, count: int = 10,
                     categories: str = '111',
                     purity: str = '110',
                     resolutions: List[str] = None) -> List[Dict]:
        """
        获取随机壁纸

        Args:
            count: 返回数量
            categories: 类别（通用/动漫/人物，如 '111'）
            purity: 纯净度（SFW/Sketchy/NSFW，如 '110'）
            resolutions: 分辨率列表

        Returns:
            壁纸信息列表
        """
        params = {
            'sorting': 'random',
            'categories': categories,
            'purity': purity,
            'page': 1,
            'seed': random.randint(0, 10000)
        }

        if resolutions:
            params['resolutions'] = ','.join(resolutions)

        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            return [{
                'id': img['id'],
                'url': img['path'],
                'full_url': img['path'],
                'download_url': img['path'],
                'author': img['uploader']['username'],
                'description': f"{img['category']} - {img['purity']}",
                'width': img['resolution'].split('x')[0],
                'height': img['resolution'].split('x')[1],
                'source': 'wallhaven'
            } for img in data.get('data', [])[:count]]

        except Exception as e:
            print(f"Wallhaven API error: {e}")
            return []

    def search(self, query: str, count: int = 10,
               categories: str = '111',
               purity: str = '110') -> List[Dict]:
        """
        搜索壁纸

        Args:
            query: 搜索关键词
            count: 返回数量
            categories: 类别
            purity: 纯净度

        Returns:
            壁纸信息列表
        """
        params = {
            'q': query,
            'page': 1,
            'categories': categories,
            'purity': purity
        }

        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            return [{
                'id': img['id'],
                'url': img['path'],
                'full_url': img['path'],
                'download_url': img['path'],
                'author': img['uploader']['username'],
                'description': f"{img['category']} - {img['purity']}",
                'width': img['resolution'].split('x')[0],
                'height': img['resolution'].split('x')[1],
                'source': 'wallhaven'
            } for img in data.get('data', [])[:count]]

        except Exception as e:
            print(f"Wallhaven search error: {e}")
            return []
