"""
辅助工具函数模块
提供常用的格式化、验证等工具函数。
"""

import re
from datetime import datetime, date


def format_amount(amount):
    """格式化金额为人民币显示（保留两位小数）"""
    if amount is None:
        return '¥0.00'
    return f'¥{amount:,.2f}'


def format_date(date_str):
    """格式化日期显示"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y年%m月%d日')
    except ValueError:
        return date_str


def get_current_month():
    """获取当前月份字符串 (YYYY-MM)"""
    return datetime.now().strftime('%Y-%m')


def get_current_date():
    """获取当前日期字符串 (YYYY-MM-DD)"""
    return date.today().isoformat()


def get_month_options():
    """生成近12个月的选择列表"""
    options = []
    now = datetime.now()
    for i in range(11, -1, -1):
        month = now.month - i
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        month_str = f'{year}-{month:02d}'
        label = f'{year}年{month}月'
        options.append((month_str, label))
    return options
