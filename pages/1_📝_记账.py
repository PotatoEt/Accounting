"""
📝 记账页面 - 添加消费或收入记录
"""

import streamlit as st
from datetime import date

# 导入数据库操作函数
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db


st.title('📝 记录收支')

# ============================================================
# 选择类型：支出 or 收入
# ============================================================
trans_type = st.radio(
    '选择记录类型',
    options=['expense', 'income'],
    format_func=lambda x: '💸 支出' if x == 'expense' else '💰 收入',
    horizontal=True,
)

# ============================================================
# 表单区域
# ============================================================
col1, col2 = st.columns([1, 1])

with col1:
    # 金额输入
    amount = st.number_input(
        '金额（元）',
        min_value=0.01,
        max_value=999999.99,
        value=None,
        step=10.0,
        format='%.2f',
        help='请输入金额，单位：人民币元',
    )

    # 日期选择
    record_date = st.date_input(
        '日期',
        value=date.today(),
        max_value=date.today(),
        help='选择这笔收支发生的日期',
    )

with col2:
    if trans_type == 'expense':
        # 支出分类选择（级联：先选大类，再选小类）
        parent_cats = db.get_parent_categories('expense')

        if parent_cats:
            # 一级分类选择
            parent_options = {f"{c['icon']} {c['name']}": c['id'] for c in parent_cats}
            selected_parent_label = st.selectbox(
                '一级分类',
                options=list(parent_options.keys()),
                help='先选择大类',
            )
            selected_parent_id = parent_options[selected_parent_label]

            # 二级分类选择
            sub_cats = db.get_sub_categories(selected_parent_id)
            if sub_cats:
                sub_options = {c['name']: c['id'] for c in sub_cats}
                selected_sub_label = st.selectbox(
                    '二级分类',
                    options=list(sub_options.keys()),
                    help='再选择具体类别',
                )
                selected_category_id = sub_options[selected_sub_label]
            else:
                st.warning('该大类下暂无二级分类，请先在设置中添加')
                selected_category_id = None
        else:
            st.warning('暂无支出分类，请先在设置中添加')
            selected_category_id = None

    else:
        # 收入分类选择（只有一级）
        income_cats = db.get_parent_categories('income')
        if income_cats:
            income_options = {f"{c['icon']} {c['name']}": c['id'] for c in income_cats}
            selected_income_label = st.selectbox(
                '收入分类',
                options=list(income_options.keys()),
                help='选择收入来源',
            )
            selected_category_id = income_options[selected_income_label]
        else:
            st.warning('暂无收入分类，请先在设置中添加')
            selected_category_id = None

# 备注（全宽）
note = st.text_input('备注（可选）', placeholder='例如：和同事一起吃的午饭', max_chars=200)

# ============================================================
# 保存按钮
# ============================================================
st.divider()

if st.button('✅ 保存记录', type='primary', use_container_width=True):
    if amount is None or amount <= 0:
        st.error('⚠️ 请输入有效的金额')
    elif selected_category_id is None:
        st.error('⚠️ 请选择分类')
    else:
        # 保存到数据库
        db.add_transaction(
            amount=amount,
            trans_type=trans_type,
            category_id=selected_category_id,
            date=record_date.isoformat(),
            note=note.strip(),
        )
        st.success(f'✅ 已保存：{amount:.2f} 元')
        st.balloons()

# ============================================================
# 底部提示
# ============================================================
st.divider()
st.caption('💡 提示：保存成功后，可以去「📋 流水」页面查看记录。')
st.caption('💡 分类不够用？去「⚙️ 设置」页面添加新分类。')
