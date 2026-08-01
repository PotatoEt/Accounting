"""
💰 预算页面 - 设置和查看月度预算
"""

import streamlit as st

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
from utils.helpers import format_amount, get_month_options, get_current_month
from utils.charts import create_budget_gauge


st.title('💰 预算管理')

# ============================================================
# 月份选择
# ============================================================
month_options = get_month_options()
selected_month = st.selectbox(
    '选择月份',
    options=[opt[0] for opt in month_options],
    format_func=lambda x: next((opt[1] for opt in month_options if opt[0] == x), x),
    index=0,
    key='budget_month',
)

st.divider()

# ============================================================
# 获取当月数据和预算
# ============================================================
expense_data = db.get_monthly_summary(selected_month, 'expense')
current_budget = db.get_budget(selected_month)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('📊 当前状态')
    st.metric('本月已支出', format_amount(expense_data['total']))

    if current_budget:
        remaining = current_budget - expense_data['total']
        percent = (expense_data['total'] / current_budget * 100) if current_budget > 0 else 0

        st.metric(
            '剩余预算',
            format_amount(remaining),
            delta=f'已用 {percent:.1f}%',
        )

        if remaining < 0:
            st.error(f'⚠️ 已超预算 {format_amount(abs(remaining))}！')
        elif percent >= 80:
            st.warning(f'⚡ 已使用 {percent:.1f}%，请注意控制开支')
        else:
            st.success(f'✅ 预算充足，剩余 {format_amount(remaining)}')

    else:
        st.info('📝 该月还未设置预算')

with col2:
    st.subheader('⚙️ 设置预算')

    # 预算设置表单
    default_amount = current_budget if current_budget else 3000.0
    new_budget = st.number_input(
        '月度预算（元）',
        min_value=100.0,
        max_value=999999.0,
        value=float(default_amount),
        step=100.0,
        format='%.2f',
        help='设置该月的总预算金额',
    )

    if st.button('💾 保存预算', type='primary', use_container_width=True):
        db.set_budget(selected_month, new_budget)
        st.success(f'✅ 已设置 {selected_month.replace("-", "年")}月 预算为 {format_amount(new_budget)}')
        st.rerun()

st.divider()

# ============================================================
# 预算仪表盘
# ============================================================
if current_budget and current_budget > 0:
    st.subheader('📊 预算仪表盘')

    gauge_fig = create_budget_gauge(
        spent=expense_data['total'],
        budget=current_budget,
        title=f'{selected_month.replace("-", "年")}月 预算使用情况',
    )
    if gauge_fig:
        st.plotly_chart(gauge_fig, use_container_width=True)

    # 按分类显示预算消耗
    if expense_data['cat_summary']:
        st.subheader('📋 分类消耗明细')
        for cat in expense_data['cat_summary']:
            cat_percent = (cat['total'] / current_budget * 100) if current_budget > 0 else 0
            cols = st.columns([3, 1, 4])
            with cols[0]:
                st.text(f"{cat.get('icon', '')} {cat['name']}")
            with cols[1]:
                st.text(format_amount(cat['total']))
            with cols[2]:
                st.progress(min(cat_percent / 100, 1.0), text=f'{cat_percent:.1f}%')

st.divider()
st.caption('💡 提示：预算按月独立设置，每个月的预算可以不同。')
st.caption('💡 超预算时会显示红色警告，80%以上会显示橙色提醒。')
