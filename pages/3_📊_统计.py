"""
📊 统计页面 - 月度消费分析报表
包含：分类占比饼图、每日趋势折线图、分类排行柱状图
"""

import streamlit as st

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
from utils.helpers import format_amount, get_month_options
from utils.charts import create_category_pie, create_daily_line, create_category_bar


st.title('📊 月度统计')

# ============================================================
# 月份选择
# ============================================================
month_options = get_month_options()
# 也加入数据库中有记录但不在近12个月内的月份
db_months = db.get_available_months()
for m in db_months:
    if m not in [opt[0] for opt in month_options]:
        month_options.append((m, m.replace('-', '年') + '月'))

# 默认选当前月
current_month = month_options[0][0]
selected_month = st.selectbox(
    '选择月份',
    options=[opt[0] for opt in month_options],
    format_func=lambda x: next((opt[1] for opt in month_options if opt[0] == x), x),
    index=0,
)

st.divider()

# ============================================================
# 概览卡片
# ============================================================
expense_data = db.get_monthly_summary(selected_month, 'expense')
income_data = db.get_monthly_summary(selected_month, 'income')

col1, col2, col3 = st.columns(3)
col1.metric('💸 月支出', format_amount(expense_data['total']))
col2.metric('💰 月收入', format_amount(income_data['total']))
col3.metric(
    '📊 月结余',
    format_amount(income_data['total'] - expense_data['total']),
    delta=f"收支比 {expense_data['total']/income_data['total']*100:.0f}%" if income_data['total'] > 0 else None,
)

st.divider()

# ============================================================
# 图表区域
# ============================================================

# 如果没有数据，给出提示
if expense_data['total'] == 0 and income_data['total'] == 0:
    st.info('📭 该月暂无收支记录，去「📝 记账」页面添加吧！')
else:
    st.subheader('📈 消费分析')

    tab1, tab2, tab3 = st.tabs(['🍩 分类占比', '📈 每日趋势', '📊 分类排行'])

    with tab1:
        if expense_data['cat_summary']:
            pie_fig = create_category_pie(
                expense_data['cat_summary'],
                title=f'{selected_month.replace("-", "年")}月 消费分类占比',
            )
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info('暂无消费数据')

    with tab2:
        if expense_data['daily_summary']:
            line_fig = create_daily_line(
                expense_data['daily_summary'],
                title=f'{selected_month.replace("-", "年")}月 每日支出趋势',
            )
            st.plotly_chart(line_fig, use_container_width=True)
        else:
            st.info('暂无消费数据')

    with tab3:
        if expense_data['cat_summary']:
            bar_fig = create_category_bar(
                expense_data['cat_summary'],
                title=f'{selected_month.replace("-", "年")}月 分类消费排行',
            )
            st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.info('暂无消费数据')

    # 收入明细
    if income_data['total'] > 0:
        st.divider()
        st.subheader('💵 收入明细')

        if income_data['cat_summary']:
            income_pie = create_category_pie(
                income_data['cat_summary'],
                title=f'{selected_month.replace("-", "年")}月 收入来源占比',
            )
            st.plotly_chart(income_pie, use_container_width=True)
