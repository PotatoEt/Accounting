"""
数据库操作模块
负责 SQLite 数据库的初始化、连接管理和所有增删改查操作。
"""

import sqlite3
import os
from datetime import datetime

# 数据库文件路径（项目根目录下的 data 文件夹）
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DB_PATH = os.path.join(DB_DIR, 'accounting.db')

# ============================================================
# 预设的分类数据（一级大类 + 二级小类）
# ============================================================

# 支出分类预设
PRESET_EXPENSE_CATEGORIES = [
    ('餐饮', '🍜', None, 1, [
        ('早餐', 1), ('午餐', 2), ('晚餐', 3),
        ('零食饮料', 4), ('外卖', 5), ('聚餐', 6),
    ]),
    ('交通', '🚗', None, 2, [
        ('公交地铁', 1), ('打车', 2), ('加油充电', 3),
        ('停车费', 4), ('火车飞机', 5),
    ]),
    ('购物', '🛒', None, 3, [
        ('服饰鞋包', 1), ('数码产品', 2), ('家居用品', 3),
        ('日用品', 4), ('美妆护肤', 5),
    ]),
    ('住房', '🏠', None, 4, [
        ('房租', 1), ('水电燃气', 2), ('物业费', 3),
        ('维修', 4), ('宽带话费', 5),
    ]),
    ('娱乐', '🎮', None, 5, [
        ('电影', 1), ('游戏', 2), ('旅游', 3),
        ('运动健身', 4), ('KTV酒吧', 5),
    ]),
    ('医疗', '🏥', None, 6, [
        ('看病挂号', 1), ('药品', 2), ('体检', 3), ('牙科', 4),
    ]),
    ('教育', '📚', None, 7, [
        ('书籍', 1), ('课程培训', 2), ('文具', 3), ('考试报名', 4),
    ]),
    ('人情', '🎁', None, 8, [
        ('送礼', 1), ('请客', 2), ('红包', 3), ('结婚生子', 4),
    ]),
    ('金融', '💰', None, 9, [
        ('保险', 1), ('贷款利息', 2), ('手续费', 3),
    ]),
    ('其他', '📦', None, 10, [
        ('快递费', 1), ('宠物', 2), ('捐赠', 3), ('其他杂项', 4),
    ]),
]

# 收入分类预设（收入只有一级分类，没有二级）
PRESET_INCOME_CATEGORIES = [
    ('工资', '💼', None, 1, []),
    ('奖金', '🎉', None, 2, []),
    ('兼职', '💻', None, 3, []),
    ('投资理财', '📈', None, 4, []),
    ('退款', '↩️', None, 5, []),
    ('红包', '🧧', None, 6, []),
    ('其他收入', '📥', None, 7, []),
]


def get_connection():
    """获取数据库连接（自动创建 data 目录）"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让查询结果可以用列名访问
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """初始化数据库：建表 + 插入预设分类（仅首次运行）"""
    conn = get_connection()
    cursor = conn.cursor()

    # ---- 建表 ----
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
            parent_id INTEGER,
            icon TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
            category_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            note TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year_month TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL
        )
    ''')

    # ---- 插入预设分类（如果分类表为空） ----
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        # 插入支出分类
        for name, icon, parent_id, sort_order, children in PRESET_EXPENSE_CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (name, type, parent_id, icon, sort_order) VALUES (?, 'expense', ?, ?, ?)",
                (name, parent_id, icon, sort_order)
            )
            parent_id_new = cursor.lastrowid
            for child_name, child_order in children:
                cursor.execute(
                    "INSERT INTO categories (name, type, parent_id, icon, sort_order) VALUES (?, 'expense', ?, '', ?)",
                    (child_name, parent_id_new, child_order)
                )

        # 插入收入分类
        for name, icon, parent_id, sort_order, children in PRESET_INCOME_CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (name, type, parent_id, icon, sort_order) VALUES (?, 'income', ?, ?, ?)",
                (name, parent_id, icon, sort_order)
            )

    conn.commit()
    conn.close()


# ============================================================
# 分类相关操作
# ============================================================

def get_parent_categories(cat_type='expense'):
    """获取一级分类列表（parent_id 为 NULL 的）"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM categories WHERE type=? AND parent_id IS NULL ORDER BY sort_order",
        (cat_type,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_sub_categories(parent_id):
    """获取某个一级分类下的所有二级小类"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM categories WHERE parent_id=? ORDER BY sort_order",
        (parent_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_categories(cat_type=None):
    """获取全部分类（可选按类型筛选）"""
    conn = get_connection()
    if cat_type:
        rows = conn.execute(
            "SELECT * FROM categories WHERE type=? ORDER BY sort_order",
            (cat_type,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM categories ORDER BY type, sort_order"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_category(name, cat_type, parent_id=None, icon=''):
    """添加新分类"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO categories (name, type, parent_id, icon, sort_order) VALUES (?, ?, ?, ?, 99)",
        (name, cat_type, parent_id, icon)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_category(cat_id, name=None, icon=None):
    """修改分类名称或图标"""
    conn = get_connection()
    if name is not None:
        conn.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id))
    if icon is not None:
        conn.execute("UPDATE categories SET icon=? WHERE id=?", (icon, cat_id))
    conn.commit()
    conn.close()


def delete_category(cat_id):
    """删除分类（同时删除其子分类，因为有 ON DELETE CASCADE）"""
    conn = get_connection()
    conn.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()


def get_category_by_id(cat_id):
    """根据 ID 获取分类信息"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ============================================================
# 交易记录相关操作
# ============================================================

def add_transaction(amount, trans_type, category_id, date, note=''):
    """添加一笔交易记录（支出或收入）"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO transactions (amount, type, category_id, date, note) VALUES (?, ?, ?, ?, ?)",
        (amount, trans_type, category_id, date, note)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_transactions(trans_type=None, start_date=None, end_date=None, limit=200):
    """
    获取交易记录列表，支持按类型和日期范围筛选
    返回结果包含分类名称，便于直接显示
    """
    conn = get_connection()
    query = '''
        SELECT t.*, c.name AS category_name, c.icon AS category_icon,
               pc.name AS parent_name, pc.icon AS parent_icon
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN categories pc ON c.parent_id = pc.id
        WHERE 1=1
    '''
    params = []

    if trans_type:
        query += " AND t.type=?"
        params.append(trans_type)
    if start_date:
        query += " AND t.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)

    query += " ORDER BY t.date DESC, t.id DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_transaction(trans_id):
    """删除一条交易记录"""
    conn = get_connection()
    conn.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
    conn.commit()
    conn.close()


def get_monthly_summary(year_month, trans_type='expense'):
    """
    获取某月的汇总数据：
    - 按一级分类汇总的金额（用于饼图）
    - 按日汇总的金额（用于折线图）
    """
    conn = get_connection()

    # 按一级分类汇总
    cat_summary = conn.execute('''
        SELECT pc.id, pc.name, pc.icon, SUM(t.amount) AS total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        LEFT JOIN categories pc ON c.parent_id = pc.id
        WHERE t.type=? AND strftime('%Y-%m', t.date)=?
        GROUP BY pc.id
        ORDER BY total DESC
    ''', (trans_type, year_month)).fetchall()

    # 按日汇总
    daily_summary = conn.execute('''
        SELECT t.date, SUM(t.amount) AS total
        FROM transactions t
        WHERE t.type=? AND strftime('%Y-%m', t.date)=?
        GROUP BY t.date
        ORDER BY t.date
    ''', (trans_type, year_month)).fetchall()

    # 该月总额
    total = conn.execute('''
        SELECT COALESCE(SUM(amount), 0) FROM transactions
        WHERE type=? AND strftime('%Y-%m', date)=?
    ''', (trans_type, year_month)).fetchone()[0]

    conn.close()
    return {
        'cat_summary': [dict(r) for r in cat_summary],
        'daily_summary': [dict(r) for r in daily_summary],
        'total': total,
    }


# ============================================================
# 预算相关操作
# ============================================================

def get_budget(year_month):
    """获取某月的预算金额"""
    conn = get_connection()
    row = conn.execute(
        "SELECT amount FROM budgets WHERE year_month=?",
        (year_month,)
    ).fetchone()
    conn.close()
    return row['amount'] if row else None


def set_budget(year_month, amount):
    """设置或更新某月预算"""
    conn = get_connection()
    conn.execute('''
        INSERT INTO budgets (year_month, amount) VALUES (?, ?)
        ON CONFLICT(year_month) DO UPDATE SET amount=?
    ''', (year_month, amount, amount))
    conn.commit()
    conn.close()


def get_available_months():
    """获取所有有交易记录的月份列表"""
    conn = get_connection()
    rows = conn.execute('''
        SELECT DISTINCT strftime('%Y-%m', date) AS month
        FROM transactions
        ORDER BY month DESC
    ''').fetchall()
    conn.close()
    return [r['month'] for r in rows]


# 模块加载时自动初始化数据库
init_db()
