"""
两步路爬虫模块
爬取苏州和上海周边的轻徒步路线数据
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
from datetime import datetime

class TwoBuluCrawler:
    """两步路爬虫"""

    def __init__(self):
        self.base_url = "https://www.2bulu.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_route_list(self, location: str = "苏州", max_distance: float = 15,
                      max_elevation: float = 800, max_duration: float = 6) -> List[Dict]:
        """
        获取路线列表

        Args:
            location: 地点（苏州/上海）
            max_distance: 最大里程（公里）
            max_elevation: 最大爬升（米）
            max_duration: 最大时长（小时）

        Returns:
            路线列表
        """
        # 搜索URL（示例，实际需要根据两步路的搜索接口调整）
        search_url = f"{self.base_url}/destination/search"

        try:
            # 尝试搜索
            params = {
                'keyword': f"{location} 徒步",
                'type': 'route',
                'page': 1
            }

            response = self.session.get(search_url, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                routes = self._parse_route_list(soup, location)

                # 过滤符合条件的路线
                filtered_routes = [
                    r for r in routes
                    if r.get('distance', 100) <= max_distance
                    and r.get('elevation', 9999) <= max_elevation
                    and r.get('duration', 10) <= max_duration
                ]

                return filtered_routes
            else:
                print(f"请求失败，状态码：{response.status_code}")
                return []

        except Exception as e:
            print(f"爬取路线列表失败：{e}")
            # 返回模拟数据用于开发测试
            return self._get_mock_routes(location)

    def _parse_route_list(self, soup: BeautifulSoup, location: str) -> List[Dict]:
        """解析路线列表页面"""
        routes = []

        # 这里需要根据实际的两步路页面结构进行解析
        # 示例代码，实际需要调整

        route_items = soup.find_all('div', class_='route-item')  # 假设的类名

        for item in route_items:
            try:
                route = {
                    'name': item.find('h3').text.strip(),
                    'distance': self._extract_number(item.find('span', class_='distance')),
                    'elevation': self._extract_number(item.find('span', class_='elevation')),
                    'duration': self._extract_number(item.find('span', class_='duration')),
                    'hot_score': random.uniform(7.0, 9.5),
                    'tags': '风景,轻松',
                    'cover_url': item.find('img')['src'] if item.find('img') else '',
                    'description': item.find('p', class_='desc').text.strip() if item.find('p', class_='desc') else '',
                    'source_url': item.find('a')['href'] if item.find('a') else '',
                    'location': location,
                    'difficulty': '初级'
                }
                routes.append(route)
            except Exception as e:
                continue

        return routes

    def _extract_number(self, element) -> Optional[float]:
        """从元素中提取数字"""
        if element:
            text = element.text.strip()
            import re
            match = re.search(r'[\d.]+', text)
            if match:
                return float(match.group())
        return None

    def _get_mock_routes(self, location: str) -> List[Dict]:
        """返回模拟路线数据（用于开发测试）"""
        if location == "苏州":
            return [
                {
                    'name': '东山环线·碧螺春茶园之旅',
                    'distance': 12.5,
                    'elevation': 650,
                    'duration': 5.5,
                    'difficulty': '初级',
                    'hot_score': 9.2,
                    'tags': '风景,茶文化,轻松',
                    'cover_url': '',
                    'description': '穿越东山茶园，欣赏太湖美景，感受茶文化',
                    'source_url': '',
                    'location': '苏州东山'
                },
                {
                    'name': '西山缥缈峰轻徒步',
                    'distance': 14.0,
                    'elevation': 780,
                    'duration': 6.0,
                    'difficulty': '初级',
                    'hot_score': 8.9,
                    'tags': '山景,太湖,观景',
                    'cover_url': '',
                    'description': '登顶缥缈峰，俯瞰太湖全景',
                    'source_url': '',
                    'location': '苏州西山'
                },
                {
                    'name': '上方山森林徒步',
                    'distance': 8.5,
                    'elevation': 350,
                    'duration': 4.0,
                    'difficulty': '初级',
                    'hot_score': 8.7,
                    'tags': '森林,亲子,轻松',
                    'cover_url': '',
                    'description': '漫步森林氧吧，适合家庭出游',
                    'source_url': '',
                    'location': '苏州上方山'
                },
                {
                    'name': '灵岩山古寺徒步',
                    'distance': 10.0,
                    'elevation': 450,
                    'duration': 4.5,
                    'difficulty': '初级',
                    'hot_score': 8.5,
                    'tags': '古迹,山景,文化',
                    'cover_url': '',
                    'description': '探访千年古寺，登高望远',
                    'source_url': '',
                    'location': '苏州灵岩山'
                },
                {
                    'name': '天平山红叶徒步',
                    'distance': 9.5,
                    'elevation': 400,
                    'duration': 4.2,
                    'difficulty': '初级',
                    'hot_score': 8.3,
                    'tags': '红叶,风景,秋季',
                    'cover_url': '',
                    'description': '秋季赏红叶绝佳去处',
                    'source_url': '',
                    'location': '苏州天平山'
                },
                {
                    'name': '旺山生态徒步',
                    'distance': 11.0,
                    'elevation': 500,
                    'duration': 5.0,
                    'difficulty': '初级',
                    'hot_score': 8.1,
                    'tags': '生态,乡村,轻松',
                    'cover_url': '',
                    'description': '走进美丽乡村，体验田园风光',
                    'source_url': '',
                    'location': '苏州旺山'
                },
                {
                    'name': '虞山古道徒步',
                    'distance': 13.5,
                    'elevation': 720,
                    'duration': 5.8,
                    'difficulty': '初级',
                    'hot_score': 7.9,
                    'tags': '古道,山景,历史',
                    'cover_url': '',
                    'description': '行走在千年古道上，感受历史沧桑',
                    'source_url': '',
                    'location': '苏州常熟虞山'
                },
                {
                    'name': '同里湖畔徒步',
                    'distance': 7.0,
                    'elevation': 200,
                    'duration': 3.5,
                    'difficulty': '初级',
                    'hot_score': 7.7,
                    'tags': '水乡,古镇,轻松',
                    'cover_url': '',
                    'description': '漫步同里湖畔，欣赏水乡风光',
                    'source_url': '',
                    'location': '苏州同里'
                },
                {
                    'name': '穹窿山轻徒步',
                    'distance': 14.5,
                    'elevation': 790,
                    'duration': 6.0,
                    'difficulty': '初级',
                    'hot_score': 7.5,
                    'tags': '山景,森林,挑战',
                    'cover_url': '',
                    'description': '苏州最高峰，视野开阔',
                    'source_url': '',
                    'location': '苏州穹窿山'
                }
            ]
        elif location == "上海":
            return [
                {
                    'name': '佘山国家森林公园',
                    'distance': 8.0,
                    'elevation': 300,
                    'duration': 4.0,
                    'difficulty': '初级',
                    'hot_score': 9.0,
                    'tags': '森林,轻松,亲子',
                    'cover_url': '',
                    'description': '上海近郊徒步首选，适合全家',
                    'source_url': '',
                    'location': '上海松江佘山'
                },
                {
                    'name': '辰山植物园徒步',
                    'distance': 6.5,
                    'elevation': 150,
                    'duration': 3.0,
                    'difficulty': '初级',
                    'hot_score': 8.8,
                    'tags': '植物园,风景,轻松',
                    'cover_url': '',
                    'description': '漫步植物园，欣赏奇花异草',
                    'source_url': '',
                    'location': '上海松江辰山'
                },
                {
                    'name': '滨江森林公园徒步',
                    'distance': 10.0,
                    'elevation': 200,
                    'duration': 4.5,
                    'difficulty': '初级',
                    'hot_score': 8.6,
                    'tags': '江景,森林,轻松',
                    'cover_url': '',
                    'description': '沿江徒步，感受江风拂面',
                    'source_url': '',
                    'location': '上海浦东滨江'
                },
                {
                    'name': '东平国家森林公园',
                    'distance': 12.0,
                    'elevation': 250,
                    'duration': 5.0,
                    'difficulty': '初级',
                    'hot_score': 8.4,
                    'tags': '森林,生态,崇明',
                    'cover_url': '',
                    'description': '崇明岛最大森林公园，天然氧吧',
                    'source_url': '',
                    'location': '上海崇明东平'
                },
                {
                    'name': '滴水湖环湖徒步',
                    'distance': 21.0,
                    'elevation': 100,
                    'duration': 5.5,
                    'difficulty': '初级',
                    'hot_score': 8.2,
                    'tags': '湖景,环湖,轻松',
                    'cover_url': '',
                    'description': '环滴水湖一周，欣赏湖光山色',
                    'source_url': '',
                    'location': '上海临港滴水湖'
                },
                {
                    'name': '顾村公园徒步',
                    'distance': 7.5,
                    'elevation': 180,
                    'duration': 3.5,
                    'difficulty': '初级',
                    'hot_score': 8.0,
                    'tags': '公园,樱花,轻松',
                    'cover_url': '',
                    'description': '春季赏樱胜地',
                    'source_url': '',
                    'location': '上海宝山顾村'
                }
            ]
        else:
            return []

    def get_route_detail(self, route_url: str) -> Optional[Dict]:
        """获取路线详情"""
        try:
            response = self.session.get(f"{self.base_url}{route_url}", timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 解析详情页面
                return self._parse_route_detail(soup)
            else:
                return None

        except Exception as e:
            print(f"爬取路线详情失败：{e}")
            return None

    def _parse_route_detail(self, soup: BeautifulSoup) -> Dict:
        """解析路线详情页面"""
        # 根据实际页面结构解析
        detail = {
            'description': '',
            'difficulty': '',
            'tips': []
        }
        return detail

    def save_routes_to_db(self, routes: List[Dict], db):
        """将路线保存到数据库"""
        for route in routes:
            # 检查是否已存在
            existing = db.get_routes(location=route['location'], limit=1)
            existing_names = [r['name'] for r in existing]

            if route['name'] not in existing_names:
                db.insert_route(route)
                print(f"已保存路线：{route['name']}")
