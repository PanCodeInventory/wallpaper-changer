"""
壁纸 API 集成
支持 Unsplash 和 Wallhaven
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
    """Unsplash API"""

    def __init__(self, access_key: str):
        super().__init__()
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com"
        self.session.headers.update({
            'Authorization': f'Client-ID {access_key}'
        })

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
                'url': img['urls']['regular'],
                'full_url': img['urls']['full'],
                'download_url': img['links']['download'],
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
                'url': img['urls']['regular'],
                'full_url': img['urls']['full'],
                'download_url': img['links']['download'],
                'author': img['user']['name'],
                'description': img.get('description') or img.get('alt_description', ''),
                'width': img['width'],
                'height': img['height'],
                'source': 'unsplash'
            } for img in results]

        except Exception as e:
            print(f"Unsplash search error: {e}")
            return []


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
