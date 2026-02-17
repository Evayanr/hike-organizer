"""
数据库操作模块
使用SQLite存储路线、活动、投票、问题库等数据
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class Database:
    """数据库管理类"""

    def __init__(self, db_path: str = "data/hike.db"):
        """初始化数据库"""
        self.db_path = db_path
        # 确保数据目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 路线表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                distance REAL,
                elevation REAL,
                duration REAL,
                difficulty TEXT,
                hot_score REAL,
                tags TEXT,
                cover_url TEXT,
                description TEXT,
                source_url TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 活动表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                route_id INTEGER,
                name TEXT NOT NULL,
                activity_date DATE,
                status TEXT DEFAULT 'planning',
                poster_url TEXT,
                vote_url TEXT,
                vote_deadline TIMESTAMP,
                group_chat_id TEXT,
                vote_month TEXT,
                selected_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (route_id) REFERENCES routes(id)
            )
        ''')

        # 投票表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_id INTEGER,
                vote_date TEXT,
                weather TEXT,
                vote_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (activity_id) REFERENCES activities(id)
            )
        ''')

        # 问题库表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                click_count INTEGER DEFAULT 0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                name TEXT,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 群消息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_chat_id TEXT,
                user_id TEXT,
                message TEXT,
                is_bot BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    # ==================== 路线相关操作 ====================

    def insert_route(self, route_data: Dict) -> int:
        """插入路线"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO routes (name, distance, elevation, duration, difficulty,
                              hot_score, tags, cover_url, description, source_url, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            route_data['name'],
            route_data.get('distance'),
            route_data.get('elevation'),
            route_data.get('duration'),
            route_data.get('difficulty'),
            route_data.get('hot_score'),
            route_data.get('tags'),
            route_data.get('cover_url'),
            route_data.get('description'),
            route_data.get('source_url'),
            route_data.get('location')
        ))

        route_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return route_id

    def get_routes(self, location: str = None, limit: int = 3, offset: int = 0,
                   max_distance: float = 15, max_elevation: float = 800, max_duration: float = 6) -> List[Dict]:
        """获取路线列表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT * FROM routes
            WHERE distance <= ? AND elevation <= ? AND duration <= ?
        '''
        params = [max_distance, max_elevation, max_duration]

        if location:
            query += ' AND location LIKE ?'
            params.append(f'%{location}%')

        query += ' ORDER BY hot_score DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        routes = []
        for row in rows:
            routes.append(dict(row))

        conn.close()
        return routes

    def get_route_by_id(self, route_id: int) -> Optional[Dict]:
        """根据ID获取路线"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    def get_routes_count(self, location: str = None,
                        max_distance: float = 15, max_elevation: float = 800, max_duration: float = 6) -> int:
        """获取路线总数"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = 'SELECT COUNT(*) FROM routes WHERE distance <= ? AND elevation <= ? AND duration <= ?'
        params = [max_distance, max_elevation, max_duration]

        if location:
            query += ' AND location LIKE ?'
            params.append(f'%{location}%')

        cursor.execute(query, params)
        count = cursor.fetchone()[0]

        conn.close()
        return count

    # ==================== 活动相关操作 ====================

    def insert_activity(self, activity_data: Dict) -> int:
        """插入活动"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO activities (route_id, name, activity_date, status, poster_url,
                                  vote_url, vote_deadline, group_chat_id, vote_month, selected_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_data.get('route_id'),
            activity_data['name'],
            activity_data.get('activity_date'),
            activity_data.get('status', 'planning'),
            activity_data.get('poster_url'),
            activity_data.get('vote_url'),
            activity_data.get('vote_deadline'),
            activity_data.get('group_chat_id'),
            activity_data.get('vote_month'),
            activity_data.get('selected_date')
        ))

        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return activity_id

    def update_activity(self, activity_id: int, update_data: Dict):
        """更新活动"""
        conn = self.get_connection()
        cursor = conn.cursor()

        set_clause = ', '.join([f'{k} = ?' for k in update_data.keys()])
        values = list(update_data.values())
        values.append(activity_id)

        cursor.execute(f'UPDATE activities SET {set_clause} WHERE id = ?', values)
        conn.commit()
        conn.close()

    def get_activity(self, activity_id: int) -> Optional[Dict]:
        """获取活动"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    def get_latest_activity(self) -> Optional[Dict]:
        """获取最新活动"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM activities ORDER BY created_at DESC LIMIT 1')
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    # ==================== 投票相关操作 ====================

    def insert_vote_options(self, activity_id: int, vote_options: List[Dict]):
        """插入投票选项"""
        conn = self.get_connection()
        cursor = conn.cursor()

        for option in vote_options:
            cursor.execute('''
                INSERT INTO votes (activity_id, vote_date, weather)
                VALUES (?, ?, ?)
            ''', (activity_id, option['date'], option['weather']))

        conn.commit()
        conn.close()

    def get_vote_options(self, activity_id: int) -> List[Dict]:
        """获取投票选项"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM votes WHERE activity_id = ? ORDER BY vote_date', (activity_id,))
        rows = cursor.fetchall()

        votes = []
        for row in rows:
            votes.append(dict(row))

        conn.close()
        return votes

    def update_vote_count(self, vote_id: int, count: int):
        """更新投票数"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE votes SET vote_count = ? WHERE id = ?', (count, vote_id))
        conn.commit()
        conn.close()

    def get_max_vote_option(self, activity_id: int) -> Optional[Dict]:
        """获取得票最多的选项"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM votes WHERE activity_id = ?
            ORDER BY vote_count DESC, id ASC LIMIT 1
        ''', (activity_id,))
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    # ==================== 问题库相关操作 ====================

    def insert_faq(self, question: str, answer: str, category: str = None) -> int:
        """插入问题"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO faq (question, answer, category)
            VALUES (?, ?, ?)
        ''', (question, answer, category))

        faq_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return faq_id

    def get_all_faq(self) -> List[Dict]:
        """获取所有问题"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM faq ORDER BY click_count DESC')
        rows = cursor.fetchall()

        faqs = []
        for row in rows:
            faqs.append(dict(row))

        conn.close()
        return faqs

    def get_faq_by_question(self, question: str) -> Optional[Dict]:
        """根据问题获取答案（模糊匹配）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM faq WHERE question LIKE ?', (f'%{question}%',))
        row = cursor.fetchone()

        # 更新点击次数
        if row:
            cursor.execute('UPDATE faq SET click_count = click_count + 1 WHERE id = ?', (row['id'],))
            conn.commit()

        conn.close()
        return dict(row) if row else None

    def increment_faq_click(self, faq_id: int):
        """增加问题点击次数"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE faq SET click_count = click_count + 1 WHERE id = ?', (faq_id,))
        conn.commit()
        conn.close()

    # ==================== 用户相关操作 ====================

    def insert_user(self, user_id: str, name: str = None, role: str = 'participant') -> int:
        """插入用户"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (user_id, name, role)
                VALUES (?, ?, ?)
            ''', (user_id, name, role))

            user_id_db = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id_db
        except sqlite3.IntegrityError:
            # 用户已存在
            conn.close()
            return None

    def get_user(self, user_id: str) -> Optional[Dict]:
        """获取用户"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()

        conn.close()
        return dict(row) if row else None

    # ==================== 群消息相关操作 ====================

    def insert_message(self, group_chat_id: str, user_id: str, message: str, is_bot: bool = False) -> int:
        """插入消息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO messages (group_chat_id, user_id, message, is_bot)
            VALUES (?, ?, ?, ?)
        ''', (group_chat_id, user_id, message, is_bot))

        msg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return msg_id

    def get_recent_messages(self, group_chat_id: str, limit: int = 50) -> List[Dict]:
        """获取最近消息"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM messages WHERE group_chat_id = ?
            ORDER BY created_at DESC LIMIT ?
        ''', (group_chat_id, limit))
        rows = cursor.fetchall()

        messages = []
        for row in rows:
            messages.append(dict(row))

        conn.close()
        return messages

    # ==================== 初始化问题库 ====================

    def init_faq_data(self):
        """初始化问题库数据"""
        # 检查是否已有数据
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM faq')
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            return

        # 基础信息类
        faqs = [
            ("活动费用多少？", "本次活动为公益性质，不收取服务费，仅收取AA制交通费用，具体金额在活动群内通知。", "费用"),
            ("需要带什么装备？", "请准备好徒步鞋、双肩背包、饮用水（1.5-2L）、午餐、防晒用品等。详细装备清单稍后发布。", "装备"),
            ("集合时间和地点？", "集合时间和地点会在活动前一天晚上群内通知，请关注群消息。", "集合"),
            ("活动难度如何？", "本次路线为轻徒步，适合新手参与，全程有领队带领。", "难度"),
            ("天气怎么样？", "活动前3天会发布天气预报，请根据天气准备相应装备。", "天气"),
            ("如何报名参加？", "报名链接将在群内发布，点击链接填写信息即可报名。", "报名"),
            ("报名截止时间？", "报名截止时间为活动前2天中午12点。", "报名"),
            ("可以带朋友吗？", "可以，请让朋友扫码进群并单独报名。", "报名"),
            ("可以取消报名吗？", "可以，请在活动前2天联系组织者取消。", "报名"),
            ("有保险吗？", "活动会为每位参与者购买户外运动保险。", "安全"),
            ("如果中途放弃怎么办？", "请告知领队，在安全地点等待或自行下撤。", "安全"),
            ("紧急联系方式？", "领队电话：[待定]，医疗救援：120", "安全"),
            ("需要准备午餐吗？", "需要，请自带午餐和适量零食。", "装备"),
            ("有厕所吗？", "路线途中可能有厕所，建议自备湿纸巾。", "其他"),
            ("可以带宠物吗？", "为了安全和环保，不建议带宠物。", "其他")
        ]

        for question, answer, category in faqs:
            self.insert_faq(question, answer, category)
