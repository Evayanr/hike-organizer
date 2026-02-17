"""
微信集成模块
通过企业微信机器人发送消息到微信群
"""

import requests
import json
from typing import Dict, List, Optional

class WeChatBot:
    """企业微信机器人"""

    def __init__(self, webhook_url: str):
        """
        初始化机器人

        Args:
            webhook_url: 企业微信机器人的webhook地址
        """
        self.webhook_url = webhook_url

    def send_text(self, content: str) -> bool:
        """
        发送文本消息

        Args:
            content: 消息内容

        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            print("未配置企业微信Webhook地址")
            return False

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                timeout=10
            )

            result = response.json()
            if result.get('errcode') == 0:
                print("文本消息发送成功")
                return True
            else:
                print(f"文本消息发送失败：{result.get('errmsg')}")
                return False

        except Exception as e:
            print(f"发送消息异常：{e}")
            return False

    def send_image(self, image_path: str) -> bool:
        """
        发送图片消息

        Args:
            image_path: 图片文件路径

        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            print("未配置企业微信Webhook地址")
            return False

        # 企业微信机器人发送图片需要先上传素材获取media_id
        # 这里简化处理，使用Markdown格式的图片链接
        # 实际使用时需要调用上传素材接口

        # 临时方案：发送图片的Markdown格式
        # 注意：这需要图片可以被公开访问
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"![海报]({image_path})"
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                timeout=10
            )

            result = response.json()
            if result.get('errcode') == 0:
                print("图片消息发送成功")
                return True
            else:
                print(f"图片消息发送失败：{result.get('errmsg')}")
                return False

        except Exception as e:
            print(f"发送图片异常：{e}")
            return False

    def send_markdown(self, content: str) -> bool:
        """
        发送Markdown格式消息

        Args:
            content: Markdown内容

        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            print("未配置企业微信Webhook地址")
            return False

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                timeout=10
            )

            result = response.json()
            if result.get('errcode') == 0:
                print("Markdown消息发送成功")
                return True
            else:
                print(f"Markdown消息发送失败：{result.get('errmsg')}")
                return False

        except Exception as e:
            print(f"发送消息异常：{e}")
            return False

    def send_welcome_message(self, route_info: Dict, activity_date: str) -> bool:
        """
        发送活动群欢迎消息

        Args:
            route_info: 路线信息
            activity_date: 活动日期

        Returns:
            是否发送成功
        """
        message = f"""🎉 欢迎大家加入本次轻徒步活动群！

本次活动信息：
📍 <font color="warning">路线</font>：{route_info.get('name', '')}
📅 <font color="info">时间</font>：{activity_date}
🏃 里程：{route_info.get('distance', 0)}公里
⛰️ 爬升：{route_info.get('elevation', 0)}米
⏱️ 时长：{route_info.get('duration', 0)}小时
💰 费用：公益免费（AA制交通费）

---

📋 常见问题快速入口：
1. 活动费用多少？
2. 需要带什么装备？
3. 集合时间和地点？
4. 活动难度如何？
5. 天气怎么样？
6. 如何报名参加？

<font color="comment">有任何问题请直接在群里提问，机器人小助手会自动回复～</font>"""

        return self.send_markdown(message)

    def send_poster_with_qrcode(self, poster_path: str, vote_url: str) -> bool:
        """
        发送海报和投票链接

        Args:
            poster_path: 海报文件路径
            vote_url: 投票链接

        Returns:
            是否发送成功
        """
        # 发送海报
        if not self.send_image(poster_path):
            return False

        # 发送投票说明
        message = f"📢 活动投票已开启！\n\n请扫描上方二维码或点击下方链接选择活动日期：\n{vote_url}"
        return self.send_markdown(message)

    def send_vote_result(self, selected_date: str, weather: str) -> bool:
        """
        发送投票结果

        Args:
            selected_date: 选中的日期
            weather: 天气情况

        Returns:
            是否发送成功
        """
        message = f"""🎉 投票结果公布！

活动日期已确定为：<font color="warning">{selected_date}</font>
天气预报：<font color="info">{weather}</font>

接下来请留意群内通知，我们会在活动前发布详细安排和集合信息。

<font color="comment">期待与大家一起出发！🚶‍♂️🚶‍♀️</font>"""

        return self.send_markdown(message)

    def send_activity_reminder(self, activity_date: str, route_info: Dict) -> bool:
        """
        发送活动提醒

        Args:
            activity_date: 活动日期
            route_info: 路线信息

        Returns:
            是否发送成功
        """
        message = f"""📢 活动前提醒！

活动时间：<font color="warning">{activity_date}</font>

<font color="info">集合信息</font>：
- 时间：活动前一天晚上群内通知
- 地点：待定

<font color="warning">装备清单</font>：
✅ 徒步鞋（防滑耐磨）
✅ 双肩背包
✅ 饮用水（1.5-2L）
✅ 午餐和零食
✅ 防晒用品
✅ 个人常用药品

<font color="comment">请提前做好准备，准时集合！</font>"""

        return self.send_markdown(message)
