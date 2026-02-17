"""
徒步活动组织系统 - 主应用
基于Streamlit的Web界面
最终修复版本 - 无ImportError、无AttributeError

修复内容：
1. 移除所有 st.终止()，替换为 st.stop()
2. 移除外部导入 insert_test_routes，使用内置测试数据
3. 确保所有Streamlit方法使用标准英文命名
"""

import streamlit as st
from datetime import datetime, timedelta
from utils.database import Database
from utils.crawler import TwoBuluCrawler
from utils.poster import PosterGenerator
from utils.weather import WeatherAPI
from utils.wechat import WeChatBot
import os
from dateutil.relativedelta import relativedelta

# ==================== 内置测试路线数据 ====================
def get_test_suzhou_routes():
    """获取苏州测试路线数据"""
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

def get_test_shanghai_routes():
    """获取上海测试路线数据"""
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

def insert_test_routes_to_db(db):
    """将测试路线数据插入数据库"""
    all_routes = get_test_suzhou_routes() + get_test_shanghai_routes()
    success_count = 0
    skip_count = 0
    
    for route in all_routes:
        try:
            # 检查是否已存在
            existing_routes = db.get_routes(location=route.get('location', ''), limit=100)
            existing_names = [r['name'] for r in existing_routes]
            
            if route['name'] in existing_names:
                skip_count += 1
            else:
                route_id = db.insert_route(route)
                success_count += 1
        except Exception as e:
            pass
    
    return {
        'success': success_count,
        'skip': skip_count,
        'total': len(all_routes)
    }

# 页面配置
st.set_page_config(
    page_title="徒步活动组织系统",
    page_icon="🚶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化数据库
@st.cache_resource
def init_db():
    # 确保数据目录存在
    os.makedirs("data", exist_ok=True)
    
    db = Database("data/hike.db")
    db.init_faq_data()
    
    # 检查是否已有路线数据，如果没有则插入测试数据
    routes_count = db.get_routes_count()
    if routes_count == 0:
        # 插入测试数据（使用内置函数）
        insert_test_routes_to_db(db)
    
    return db

db = init_db()

# 初始化工具类
@st.cache_resource
def init_tools():
    return {
        'crawler': TwoBuluCrawler(),
        'poster': PosterGenerator(),
        'weather': WeatherAPI(api_key=os.getenv('WEATHER_API_KEY', '')),
        'wechat': WeChatBot(webhook_url=os.getenv('WECHAT_WEBHOOK_URL', ''))
    }

tools = init_tools()

# ==================== 侧边栏配置 ====================
st.sidebar.title("🚶 徒步活动组织系统")
st.sidebar.markdown("---")

# 组织者信息
st.sidebar.subheader("组织者信息")
organizer_name = st.sidebar.text_input("组织者昵称", "活动组织者")

# 微信配置
st.sidebar.subheader("微信配置")
wechat_webhook = st.sidebar.text_input(
    "企业微信Webhook URL",
    type="password",
    help="企业微信机器人的Webhook地址"
)
if wechat_webhook:
    tools['wechat'].webhook_url = wechat_webhook

# 天气API配置
st.sidebar.subheader("天气API")
weather_api_key = st.sidebar.text_input(
    "和风天气API Key",
    type="password",
    help="和风天气API密钥"
)
if weather_api_key:
    tools['weather'].api_key = weather_api_key

st.sidebar.markdown("---")
st.sidebar.markdown("### 系统说明")
st.sidebar.markdown("""
- 轻徒步定义：当天来回，不住宿，天黑前下山
- 活动定位：公益性质，不收取服务费
- 目标用户：苏州和上海周边徒步爱好者
""")

# ==================== 主界面 ====================
st.title("🏔️ 活动组织流程")

# 创建多页面标签页
tab1, tab2, tab3 = st.tabs(["路线选择", "海报制作", "投票与建群"])

# ==================== 标签页1：路线选择 ====================
with tab1:
    st.header("📍 步骤1：选择路线")

    # 选择地点
    col1, col2 = st.columns([1, 3])
    with col1:
        location = st.selectbox("选择地点", ["苏州", "上海"])
    with col2:
        st.write(f"将为您推荐{location}周边的轻徒步路线")

    st.markdown("---")

    # 加载路线按钮
    if st.button("🔄 刷新路线", type="primary"):
        with st.spinner("正在从两步路获取最新路线..."):
            routes = tools['crawler'].get_route_list(location=location)

            # 保存到数据库
            for route in routes:
                db.insert_route(route)

            st.success(f"已获取 {len(routes)} 条路线！")
            st.rerun()

    # 获取路线列表
    routes = db.get_routes(location=location, limit=3, offset=st.session_state.get('route_offset', 0))

    # 显示路线列表
    if routes:
        st.subheader(f"推荐路线（按热度排序）")

        for i, route in enumerate(routes, 1):
            with st.container():
                # 路线卡片
                col_a, col_b, col_c = st.columns([3, 2, 1])

                with col_a:
                    st.write(f"### {i}. {route['name']}")
                    st.caption(route.get('description', ''))

                with col_b:
                    st.metric("里程", f"{route['distance']}公里")
                    st.metric("爬升", f"{route['elevation']}米")
                    st.metric("时长", f"{route['duration']}小时")

                with col_c:
                    difficulty_color = {
                        '初级': '🟢',
                        '中级': '🟡',
                        '高级': '🟠',
                        '专业级': '🔴'
                    }
                    st.write(difficulty_color.get(route['difficulty'], '') + " " + route['difficulty'])
                    st.metric("热度", f"{route['hot_score']:.1f}")

                st.markdown("---")

        # 分页控制
        total_count = db.get_routes_count(location=location)
        if total_count > 3:
            col_left, col_center, col_right = st.columns([1, 2, 1])

            with col_left:
                if st.button("⬅️ 上一页"):
                    current_offset = st.session_state.get('route_offset', 0)
                    if current_offset > 0:
                        st.session_state['route_offset'] = current_offset - 3
                        st.rerun()

            with col_center:
                st.write(f"显示 1-{min(3, total_count)} / 共 {total_count} 条")

            with col_right:
                if st.button("➡️ 下一页"):
                    current_offset = st.session_state.get('route_offset', 0)
                    if current_offset + 3 < total_count:
                        st.session_state['route_offset'] = current_offset + 3
                        st.rerun()
    else:
        st.info("暂无路线数据，请点击上方「刷新路线」按钮获取")

    # 选择路线
    st.subheader("选择路线")
    all_routes = db.get_routes(location=location, limit=100)
    if all_routes:
        route_names = [r['name'] for r in all_routes]
        selected_route_name = st.selectbox("选择一条路线", route_names)

        if selected_route_name:
            selected_route = next((r for r in all_routes if r['name'] == selected_route_name), None)
            if selected_route and st.button("确认选择", type="primary"):
                st.session_state['selected_route'] = selected_route
                st.success(f"已选择：{selected_route_name}")
                st.info("👉 请前往「海报制作」标签页继续")
    else:
        st.warning("请先获取路线数据")

# ==================== 标签页2：海报制作 ====================
with tab2:
    st.header("🎨 步骤2：制作海报")

    # 检查是否已选择路线
    if 'selected_route' not in st.session_state:
        st.warning("请先在「路线选择」标签页选择一条路线")
        st.stop()

    selected_route = st.session_state['selected_route']

    # 显示选中的路线信息
    st.info(f"已选择路线：{selected_route['name']}")

    # 步骤2.1：生成主题词
    st.subheader("📝 2.1 选择主题词")

    # 生成主题词
    themes = tools['poster'].generate_themes(selected_route)

    # 显示主题词选择
    selected_theme = st.selectbox("选择一个主题词", themes + ["自定义"])

    # 如果选择自定义
    if selected_theme == "自定义":
        custom_theme = st.text_input("输入自定义主题词")
        if custom_theme:
            selected_theme = custom_theme

    st.success(f"已选择主题词：{selected_theme}")

    # 步骤2.2：选择背景图
    st.subheader("🖼️ 2.2 选择背景图片")

    # 搜索图片
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔍 搜索图片", type="primary"):
            with st.spinner("正在搜索图片..."):
                images = tools['poster'].search_images(selected_theme, count=3)
                st.session_state['searched_images'] = images
                st.success(f"找到 {len(images)} 张图片")

    with col2:
        uploaded_image = st.file_uploader("或上传自定义图片", type=['jpg', 'jpeg', 'png'])

    # 显示搜索结果或上传的图片
    background_image = None

    if uploaded_image:
        background_image = tools['poster'].upload_custom_image(uploaded_image)
        st.success("已上传自定义图片")
    elif 'searched_images' in st.session_state:
        st.write("搜索结果：")
        cols = st.columns(3)
        for i, img_url in enumerate(st.session_state['searched_images']):
            with cols[i]:
                st.image(img_url, use_column_width=True)
                if st.button(f"选择图片 {i+1}", key=f"img_{i}"):
                    background_image = tools['poster'].download_image(img_url)
                    st.session_state['selected_bg_image'] = background_image
                    st.success(f"已选择图片 {i+1}")
    else:
        st.info("请搜索图片或上传自定义图片")

    if background_image:
        st.session_state['selected_bg_image'] = background_image

    # 步骤2.3：选择投票月份
    st.subheader("📅 2.3 选择投票月份")

    # 获取下个月
    next_month = datetime.now() + relativedelta(months=1)
    default_year = next_month.year
    default_month = next_month.month

    col1, col2 = st.columns([1, 1])
    with col1:
        vote_year = st.number_input("年份", value=default_year, min_value=2024, max_value=2030)
    with col2:
        vote_month = st.number_input("月份", value=default_month, min_value=1, max_value=12)

    st.write(f"将生成 {vote_year}年{vote_month}月 的所有周六和周日作为投票选项")

    # 步骤2.4：生成投票选项
    st.subheader("📋 2.4 生成投票选项")

    if st.button("🔄 生成投票选项", type="primary"):
        with st.spinner("正在获取天气信息..."):
            vote_options = tools['weather'].generate_vote_options(vote_year, vote_month, location)
            st.session_state['vote_options'] = vote_options
            st.success(f"已生成 {len(vote_options)} 个投票选项")

    # 显示投票选项
    if 'vote_options' in st.session_state:
        st.write("投票选项预览：")
        for option in st.session_state['vote_options']:
            st.write(f"- {option['date']}：{option['weather']}")

    # 步骤2.5：设置投票截止时间
    st.subheader("⏰ 2.5 设置投票截止时间")

    # 默认5天后
    default_deadline = datetime.now() + timedelta(days=5)
    vote_deadline = st.datetime_input(
        "投票截止时间",
        value=default_deadline,
        min_value=datetime.now() + timedelta(days=1)
    )

    st.write(f"投票将在 {vote_deadline.strftime('%Y-%m-%d %H:%M')} 截止")

    # 步骤2.6：生成海报
    st.subheader("🖼️ 2.6 生成海报")

    if all([
        'selected_bg_image' in st.session_state,
        'vote_options' in st.session_state
    ]):
        if st.button("✨ 生成海报", type="primary"):
            with st.spinner("正在生成海报..."):
                # 创建投票链接（示例）
                vote_url = f"https://example.com/vote/{int(datetime.now().timestamp())}"

                # 生成海报
                poster_path = tools['poster'].generate_poster(
                    selected_route,
                    selected_theme,
                    st.session_state['selected_bg_image'],
                    vote_url,
                    st.session_state['vote_options']
                )

                st.session_state['poster_path'] = poster_path
                st.session_state['vote_url'] = vote_url
                st.session_state['vote_deadline'] = vote_deadline
                st.session_state['vote_year'] = vote_year
                st.session_state['vote_month'] = vote_month

                st.success("海报生成成功！")
                st.image(poster_path, use_column_width=True)
                st.info("👉 请前往「投票与建群」标签页继续")
    else:
        st.warning("请先完成上述步骤：选择背景图片和生成投票选项")

# ==================== 标签页3：投票与建群 ====================
with tab3:
    st.header("📊 步骤3：投票与建群")

    # 检查是否已生成海报
    if 'poster_path' not in st.session_state:
        st.warning("请先在「海报制作」标签页生成海报")
        st.stop()

    # 显示海报
    st.subheader("📋 活动海报预览")
    st.image(st.session_state['poster_path'], use_column_width=True)

    # 步骤3.1：发布海报到微信群
    st.subheader("💬 3.1 发布海报到微信群")

    if st.button("📤 发布海报", type="primary"):
        with st.spinner("正在发布海报..."):
            success = tools['wechat'].send_poster_with_qrcode(
                st.session_state['poster_path'],
                st.session_state['vote_url']
            )

            if success:
                st.success("海报已发布到微信群！")
                st.session_state['poster_published'] = True
            else:
                st.error("发布失败，请检查微信Webhook配置")

    # 步骤3.2：监控投票
    st.subheader("📊 3.2 投票监控")

    if 'poster_published' in st.session_state:
        st.info(f"投票截止时间：{st.session_state['vote_deadline'].strftime('%Y-%m-%d %H:%M')}")

        # 显示投票选项
        if 'vote_options' in st.session_state:
            st.write("当前投票选项：")
            for i, option in enumerate(st.session_state['vote_options'], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{i}. {option['date']} - {option['weather']}")
                with col2:
                    # 模拟投票数（实际需要从投票平台获取）
                    vote_count = st.number_input(
                        "票数",
                        min_value=0,
                        value=0,
                        key=f"vote_{i}",
                        label_visibility="collapsed"
                    )

            # 确定日期按钮
            if st.button("📊 确定活动日期", type="primary"):
                st.success("活动日期已确定！")
                st.info("👉 请等待系统自动创建活动群")

    # 步骤3.3：创建活动群
    st.subheader("👥 3.3 创建活动群")

    # 获取得票最多的日期
    if 'vote_options' in st.session_state:
        # 模拟选择（实际应该从投票结果获取）
        vote_options = st.session_state['vote_options']
        selected_date = st.selectbox(
            "选择活动日期（如果有平票，请手动选择）",
            [opt['date'] for opt in vote_options]
        )

        if st.button("🚀 创建活动群并发送欢迎消息", type="primary"):
            with st.spinner("正在创建活动群..."):
                # 获取天气
                selected_date_obj = datetime.strptime(selected_date.split('（')[0], "%Y-%m-%d")
                weather = tools['weather'].get_weather(
                    selected_date_obj.strftime("%Y-%m-%d"),
                    st.session_state.get('selected_route', {}).get('location', '苏州')
                )

                # 发送欢迎消息
                success = tools['wechat'].send_welcome_message(
                    st.session_state['selected_route'],
                    selected_date
                )

                if success:
                    st.success("活动群创建成功！")
                    st.success(f"欢迎消息已发送")

                    # 显示活动信息
                    st.markdown("---")
                    st.subheader("🎉 活动创建成功！")

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.write("**活动信息**")
                        st.write(f"📍 路线：{st.session_state['selected_route']['name']}")
                        st.write(f"📅 日期：{selected_date}")
                        st.write(f"🌤️ 天气：{weather}")

                    with col2:
                        st.write("**群聊信息**")
                        st.write(f"👥 群聊：{st.session_state['selected_route']['name']}活动群")
                        st.write(f"🤖 机器人：已加入并激活")

                    # 保存活动到数据库
                    activity_data = {
                        'route_id': st.session_state['selected_route']['id'],
                        'name': f"{st.session_state['selected_route']['name']} - {selected_date}",
                        'activity_date': selected_date.split('（')[0],
                        'status': 'recruiting',
                        'poster_url': st.session_state['poster_path'],
                        'vote_url': st.session_state['vote_url'],
                        'vote_deadline': st.session_state['vote_deadline'],
                        'vote_month': f"{st.session_state['vote_year']}-{st.session_state['vote_month']}",
                        'selected_date': selected_date
                    }

                    activity_id = db.insert_activity(activity_data)

                    # 保存投票选项
                    db.insert_vote_options(activity_id, st.session_state['vote_options'])

                    st.success(f"活动已保存到数据库（ID: {activity_id}）")

                    st.info("🎊 现在机器人小助手已经准备好回答群成员的问题了！")
                else:
                    st.error("创建活动群失败，请检查微信Webhook配置")

# ==================== 底部信息 ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>徒步活动组织系统 v1.0 | 公益徒步 · 安全第一 · 快乐同行</p>
</div>
""", unsafe_allow_html=True)
