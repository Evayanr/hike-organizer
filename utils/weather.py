"""
天气API模块
获取指定日期的天气预报
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import calendar

class WeatherAPI:
    """天气API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # 使用免费的和风天气API
        self.base_url = "https://devapi.qweather.com/v7"

    def get_weather(self, date: str, location: str = "苏州") -> str:
        """
        获取指定日期的天气预报

        Args:
            date: 日期（格式：YYYY-MM-DD）
            location: 地点

        Returns:
            天气描述字符串
        """
        # 和风天气API需要城市ID
        # 苏州: 101190401, 上海: 101020100
        city_ids = {
            "苏州": "101190401",
            "上海": "101020100"
        }
        city_id = city_ids.get(location, "101190401")

        try:
            # 调用7天天气预报API
            url = f"{self.base_url}/weather/7d"
            params = {
                'location': city_id,
                'key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '200':
                    for day in data['daily']:
                        if day['fxDate'] == date:
                            temp_min = day['tempMin']
                            temp_max = day['tempMax']
                            text_day = day['textDay']
                            return f"{text_day}，{temp_min}-{temp_max}℃"

            return "天气暂无数据"

        except Exception as e:
            print(f"获取天气失败：{e}")
            return "天气暂无数据"

    def get_weekends(self, year: int, month: int) -> List[str]:
        """
        获取指定月份的所有周六和周日

        Args:
            year: 年份
            month: 月份

        Returns:
            日期列表（格式：YYYY-MM-DD）
        """
        weekends = []

        # 获取该月的天数
        days_in_month = calendar.monthrange(year, month)[1]

        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            weekday = date.weekday()

            # 周六(5)和周日(6)
            if weekday in [5, 6]:
                weekends.append(date.strftime("%Y-%m-%d"))

        return weekends

    def generate_vote_options(self, year: int, month: int, location: str = "苏州") -> List[Dict]:
        """
        生成投票选项（包含日期和天气）

        Args:
            year: 年份
            month: 月份
            location: 地点

        Returns:
            投票选项列表
        """
        weekends = self.get_weekends(year, month)
        options = []

        for date in weekends:
            # 获取星期几
            dt = datetime.strptime(date, "%Y-%m-%d")
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[dt.weekday()]

            # 获取天气
            weather = self.get_weather(date, location)

            # 添加星期几到日期中
            date_with_weekday = f"{date}（{weekday}）"

            options.append({
                'date': date_with_weekday,
                'weather': weather,
                'date_only': date  # 用于后续排序
            })

        return options
