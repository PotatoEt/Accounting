"""
📋 流水页面 - 查看和删除收支记录
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
from utils.helpers import format_amount, format_date


st.title('📋 收支流水')

# ============================================================
# 筛选区域
# ============================================================
col1, col2, col3 = st.columns(3)

with col1:
    filter_type = st.selectbox(
        '记录类型',
        options=['all', 'expense', 'income'],
        format_func=lambda x: {'all': '全部', 'expense': '💸 仅支出', 'income': '💰 仅收入'}[x],
    )

with col2:
    # 日期范围快捷选择
    date_range = st.selectbox(
        '日期范围',
        options=['本月', '上月', '近7天', '近30天', '全部'],
        index=0,
    )

with col3:
    # 记录数量限制
    show_count = st.selectbox('显示条数', options=[20, 50, 100, 200], index=1)

# 根据日期范围选项计算起止日期
today = date.today()
start_date = None
end_date = None

if date_range == '本月':
    start_date = today.replace(day=1).isoformat()
elif date_range == '上月':
    first_of_this_month = today.replace(day=1)
    last_month_last_day = first_of_this_month - timedelta(days=1)
    start_date = last_month_last_day.replace(day=1).isoformat()
    end_date = last_month_last_day.isoformat()
elif date_range == '近7天':
    start_date = (today - timedelta(days=6)).isoformat()
elif date_range == '近30天':
    start_date = (today - timedelta(days=29)).isoformat()

# ============================================================
# 加载数据
# ============================================================
trans_type_arg = None if filter_type == 'all' else filter_type
records = db.get_transactions(
    trans_type=trans_type_arg,
    start_date=start_date,
    end_date=end_date,
    limit=show_count,
)

# ============================================================
# 汇总统计
# ============================================================
if records:
    total_expense = sum(r['amount'] for r in records if r['type'] == 'expense')
    total_income = sum(r['amount'] for r in records if r['type'] == 'income')

    col_e, col_i, col_b = st.columns(3)
    col_e.metric('💸 支出合计', format_amount(total_expense))
    col_i.metric('💰 收入合计', format_amount(total_income))
    col_b.metric('📊 结余', format_amount(total_income - total_expense))

st.divider()

# ============================================================
# 记录列表
# ============================================================
if not records:
    st.info('📭 暂无记录，去「📝 记账」页面添加吧！')
else:
    st.caption(f'共找到 {len(records)} 条记录')

    for record in records:
        is_expense = record['type'] == 'expense'

        # 每行一个卡片
        with st.container():
            cols = st.columns([1, 3, 1])

            with cols[0]:
                # 金额显示（红色支出，绿色收入）
                if is_expense:
                    st.markdown(f'### 🔴 {format_amount(record["amount"])}')
                else:
                    st.markdown(f'### 🟢 {format_amount(record["amount"])}')

            with cols[1]:
                # 分类和备注
                parent_info = ''
                if record.get('parent_name'):
                    parent_info = f'{record.get("parent_icon", "")} {record["parent_name"]} → '

                cat_display = f'{parent_info}{record.get("category_icon", "")} {record["category_name"]}'
                st.markdown(f'**{cat_display}**')
                st.caption(f'📅 {format_date(record["date"])}')
                if record['note']:
                    st.caption(f'💬 {record["note"]}')

            with cols[2]:
                # 删除按钮
                delete_key = f'delete_{record["id"]}'
                if st.button('🗑️ 删除', key=delete_key, type='secondary'):
                    db.delete_transaction(record['id'])
                    st.success('已删除')
                    st.rerun()

            st.divider()

# ============================================================
# 底部提示
# ============================================================
st.caption('💡 提示：点击删除按钮会立即删除，无法撤销，请确认后再操作。')
