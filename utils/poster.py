"""
海报生成模块
根据路线信息、主题词、背景图、投票二维码合成海报
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
from typing import Dict, List, Optional
import os
import requests
from io import BytesIO

class PosterGenerator:
    """海报生成器"""

    def _load_font(self, size):
        """加载字体，支持多种系统"""
        # 尝试多种字体路径
        font_paths = [
            # Linux 系统字体
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            # macOS 系统字体
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            # Windows 系统字体
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        # 如果都失败，使用默认字体
        print(f"警告：无法加载字体，使用默认字体")
        return ImageFont.load_default()

    def __init__(self):
        self.poster_width = 1080  # 海报宽度
        self.poster_height = 1920  # 海报高度
        self.assets_dir = "assets"

        # 确保资源目录存在
        os.makedirs(self.assets_dir, exist_ok=True)

        # 字体设置 - 支持Linux环境
        self.title_font = self._load_font(72)
        self.subtitle_font = self._load_font(48)
        self.content_font = self._load_font(36)
        self.small_font = self._load_font(28)
        """
        根据路线信息生成主题词

        Args:
            route_info: 路线信息

        Returns:
            主题词列表
        """
        route_name = route_info.get('name', '')
        tags = route_info.get('tags', '')
        location = route_info.get('location', '')

        # 基于路线特征生成主题词
        themes = []

        # 季节主题
        themes.extend([
            "春日赏花",
            "山野徒步",
            "周末逃离",
            "自然疗愈"
        ])

        # 根据标签生成
        if '风景' in tags:
            themes.append("绝美风光")
        if '茶文化' in tags:
            themes.append("茶香之旅")
        if '古镇' in tags or '文化' in tags:
            themes.append("文化探索")
        if '亲子' in tags:
            themes.append("亲子时光")
        if '轻松' in tags:
            themes.append("轻松休闲")

        # 根据位置生成
        if '苏州' in location:
            themes.append("苏式生活")
        if '上海' in location:
            themes.append("都市绿洲")

        # 去重并返回前6个
        themes = list(set(themes))
        return themes[:6]

    def search_images(self, theme: str, count: int = 3) -> List[str]:
        """
        根据主题词搜索图片

        Args:
            theme: 主题词
            count: 图片数量

        Returns:
            图片URL列表
        """
        # 这里使用Pexels API（需要配置API Key）
        # 暂时返回示例URL，实际需要调用API

        # Pexels API调用示例（需要API Key）
        # api_key = "YOUR_PEXELS_API_KEY"
        # url = f"https://api.pexels.com/v1/search?query={theme}&per_page={count}"
        # headers = {"Authorization": api_key}
        # response = requests.get(url, headers=headers)
        # data = response.json()
        # return [photo['src']['large'] for photo in data['photos']]

        # 临时返回示例URL
        sample_images = {
            "春日赏花": [
                "https://images.pexels.com/photos/1366957/pexels-photo-1366957.jpeg",
                "https://images.pexels.com/photos/1470726/pexels-photo-1470726.jpeg",
                "https://images.pexels.com/photos/1856086/pexels-photo-1856086.jpeg"
            ],
            "山野徒步": [
                "https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg",
                "https://images.pexels.com/photos/1687855/pexels-photo-1687855.jpeg",
                "https://images.pexels.com/photos/1511311/pexels-photo-1511311.jpeg"
            ],
            "周末逃离": [
                "https://images.pexels.com/photos/162436/pexels-photo-162436.jpeg",
                "https://images.pexels.com/photos/1408221/pexels-photo-1408221.jpeg",
                "https://images.pexels.com/photos/1470111/pexels-photo-1470111.jpeg"
            ],
            "自然疗愈": [
                "https://images.pexels.com/photos/1547813/pexels-photo-1547813.jpeg",
                "https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg",
                "https://images.pexels.com/photos/1444724/pexels-photo-1444724.jpeg"
            ]
        }

        if theme in sample_images:
            return sample_images[theme][:count]
        else:
            # 默认图片
            return [
                "https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg",
                "https://images.pexels.com/photos/1687855/pexels-photo-1687855.jpeg",
                "https://images.pexels.com/photos/1511311/pexels-photo-1511311.jpeg"
            ][:count]

    def download_image(self, url: str) -> Optional[Image.Image]:
        """下载图片"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"下载图片失败：{e}")
        return None

    def generate_qrcode(self, vote_url: str) -> Image.Image:
        """
        生成投票二维码

        Args:
            vote_url: 投票链接

        Returns:
            二维码图片
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(vote_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def generate_poster(self, route_info: Dict, theme: str, background_image: Image.Image,
                       vote_url: str, vote_options: List[Dict]) -> str:
        """
        生成海报

        Args:
            route_info: 路线信息
            theme: 主题词
            background_image: 背景图片
            vote_url: 投票链接
            vote_options: 投票选项列表

        Returns:
            海报文件路径
        """
        # 创建海报画布
        poster = Image.new('RGB', (self.poster_width, self.poster_height), color='white')
        draw = ImageDraw.Draw(poster)

        # 处理背景图（调整大小并添加半透明遮罩）
        bg_image = background_image.resize((self.poster_width, self.poster_height))
        bg_image.putalpha(128)  # 半透明
        poster.paste(bg_image, (0, 0))

        # 添加深色渐变遮罩
        overlay = Image.new('RGBA', (self.poster_width, self.poster_height), (0, 0, 0, 100))
        poster.paste(overlay, (0, 0), overlay)

        # 绘制主题词（顶部）
        theme_text = theme
        theme_bbox = draw.textbbox((0, 0), theme_text, font=self.title_font)
        theme_width = theme_bbox[2] - theme_bbox[0]
        theme_x = (self.poster_width - theme_width) // 2
        draw.text((theme_x, 100), theme_text, fill='white', font=self.title_font)

        # 绘制路线名称
        route_name = route_info.get('name', '')
        name_bbox = draw.textbbox((0, 0), route_name, font=self.subtitle_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (self.poster_width - name_width) // 2
        draw.text((name_x, 200), route_name, fill='white', font=self.subtitle_font)

        # 绘制路线信息（卡片样式）
        self._draw_route_info_card(draw, route_info, 350)

        # 绘制投票选项
        self._draw_vote_options(draw, vote_options, 700)

        # 生成并绘制二维码
        qr_image = self.generate_qrcode(vote_url)
        qr_size = 250
        qr_image = qr_image.resize((qr_size, qr_size))
        qr_x = (self.poster_width - qr_size) // 2
        qr_y = 1450
        poster.paste(qr_image, (qr_x, qr_y))

        # 绘制二维码说明
        qr_text = "扫码选择活动日期"
        qr_text_bbox = draw.textbbox((0, 0), qr_text, font=self.content_font)
        qr_text_width = qr_text_bbox[2] - qr_text_bbox[0]
        qr_text_x = (self.poster_width - qr_text_width) // 2
        draw.text((qr_text_x, 1720), qr_text, fill='white', font=self.content_font)

        # 绘制底部信息
        bottom_text = "公益徒步 · 安全第一 · 快乐同行"
        bottom_bbox = draw.textbbox((0, 0), bottom_text, font=self.small_font)
        bottom_width = bottom_bbox[2] - bottom_bbox[0]
        bottom_x = (self.poster_width - bottom_width) // 2
        draw.text((bottom_x, 1850), bottom_text, fill='white', font=self.small_font)

        # 保存海报
        timestamp = int(datetime.now().timestamp())
        filename = f"poster_{timestamp}.png"
        filepath = os.path.join(self.assets_dir, filename)
        poster.save(filepath)

        return filepath

    def _draw_route_info_card(self, draw: ImageDraw.Draw, route_info: Dict, y: int):
        """绘制路线信息卡片"""
        # 卡片背景
        card_margin = 40
        card_height = 250
        draw.rounded_rectangle(
            [(card_margin, y), (self.poster_width - card_margin, y + card_height)],
            radius=20,
            fill='white',
            outline=(200, 200, 200),
            width=2
        )

        # 路线信息
        distance = route_info.get('distance', 0)
        elevation = route_info.get('elevation', 0)
        duration = route_info.get('duration', 0)
        difficulty = route_info.get('difficulty', '初级')

        info_text = [
            f"📍 路线：{route_info.get('name', '')}",
            f"🏃 里程：{distance}公里 | 爬升：{elevation}米",
            f"⏱️ 时长：{duration}小时 | 难度：{difficulty}"
        ]

        current_y = y + 50
        for text in info_text:
            draw.text((80, current_y), text, fill=(50, 50, 50), font=self.content_font)
            current_y += 60

    def _draw_vote_options(self, draw: ImageDraw.Draw, vote_options: List[Dict], y: int):
        """绘制投票选项"""
        # 标题
        draw.text((60, y), "📅 活动日期投票", fill='white', font=self.subtitle_font)

        current_y = y + 70

        # 只显示前4个选项
        for i, option in enumerate(vote_options[:4]):
            # 选项卡片
            card_margin = 40
            card_height = 80
            card_y = current_y + i * (card_height + 15)

            draw.rounded_rectangle(
                [(card_margin, card_y), (self.poster_width - card_margin, card_y + card_height)],
                radius=10,
                fill='rgba(255, 255, 255, 0.9)'
            )

            # 选项内容
            date_text = option.get('date', '')
            weather_text = option.get('weather', '')

            draw.text((70, card_y + 15), date_text, fill=(50, 50, 50), font=self.content_font)
            draw.text((70, card_y + 45), weather_text, fill=(100, 100, 100), font=self.small_font)

    def upload_custom_image(self, uploaded_file) -> Optional[Image.Image]:
        """上传自定义图片"""
        try:
            return Image.open(uploaded_file)
        except Exception as e:
            print(f"上传图片失败：{e}")
            return None
