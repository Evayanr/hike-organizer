"""
插入测试路线数据脚本
直接向数据库插入测试路线，不依赖爬虫
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import Database

def insert_suzhou_routes():
    """插入苏州测试路线"""
    routes = [
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

    return routes

def insert_shanghai_routes():
    """插入上海测试路线"""
    routes = [
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

    return routes

def main():
    """主函数"""
    print("=" * 50)
    print("开始插入测试路线数据...")
    print("=" * 50)

    # 初始化数据库
    db = Database("data/hike.db")

    # 获取所有测试路线
    all_routes = insert_suzhou_routes() + insert_shanghai_routes()

    # 插入路线
    success_count = 0
    skip_count = 0

    for route in all_routes:
        try:
            # 检查是否已存在
            existing_routes = db.get_routes(location=route['location'], limit=100)
            existing_names = [r['name'] for r in existing_routes]

            if route['name'] in existing_names:
                print(f"⏭️  跳过：{route['name']}（已存在）")
                skip_count += 1
            else:
                route_id = db.insert_route(route)
                print(f"✅ 成功插入：{route['name']} (ID: {route_id})")
                success_count += 1
        except Exception as e:
            print(f"❌ 插入失败：{route['name']} - {e}")

    print("=" * 50)
    print(f"插入完成！")
    print(f"✅ 成功插入：{success_count} 条")
    print(f"⏭️  跳过：{skip_count} 条")
    print("=" * 50)

    # 验证插入结果
    print("\n验证数据库中的路线数据：")
    print("-" * 50)

    # 查询苏州路线
    suzhou_routes = db.get_routes(location="苏州", limit=10)
    print(f"\n苏州路线（{len(suzhou_routes)}条）：")
    for route in suzhou_routes:
        print(f"  - {route['name']}")

    # 查询上海路线
    shanghai_routes = db.get_routes(location="上海", limit=10)
    print(f"\n上海路线（{len(shanghai_routes)}条）：")
    for route in shanghai_routes:
        print(f"  - {route['name']}")

    print("-" * 50)
    print("✅ 数据验证完成！")
    print("\n现在可以在 Streamlit 应用中刷新路线列表了！")

if __name__ == "__main__":
    main()
