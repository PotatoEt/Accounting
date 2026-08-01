"""
⚙️ 设置页面 - 分类管理
支持添加、修改、删除支出和收入分类
"""

import streamlit as st

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db


st.title('⚙️ 分类管理')

# ============================================================
# 选择管理类型
# ============================================================
tab1, tab2 = st.tabs(['💸 支出分类', '💰 收入分类'])

# -------- 支出分类管理 --------
with tab1:
    st.subheader('支出分类（两级）')

    parent_cats = db.get_parent_categories('expense')

    # 添加新的一级分类
    with st.expander('➕ 添加新的一级分类'):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_parent_name = st.text_input('分类名称', placeholder='例如：宠物', key='new_expense_parent_name')
        with col2:
            new_parent_icon = st.text_input('图标', placeholder='🐱', max_chars=2, key='new_expense_parent_icon')
        if st.button('添加一级分类', key='add_expense_parent'):
            if new_parent_name.strip():
                db.add_category(new_parent_name.strip(), 'expense', parent_id=None, icon=new_parent_icon.strip())
                st.success(f'✅ 已添加一级分类: {new_parent_name}')
                st.rerun()
            else:
                st.error('⚠️ 请输入分类名称')

    st.divider()

    # 显示现有分类
    if not parent_cats:
        st.info('暂无支出分类')
    else:
        for parent in parent_cats:
            sub_cats = db.get_sub_categories(parent['id'])

            with st.container():
                cols = st.columns([4, 2, 2, 1])

                with cols[0]:
                    st.markdown(f'### {parent["icon"]} {parent["name"]}')
                with cols[1]:
                    st.caption(f'{len(sub_cats)} 个二级分类')
                with cols[2]:
                    # 修改一级分类名称
                    new_name = st.text_input(
                        '改名',
                        value=parent['name'],
                        key=f'edit_parent_{parent["id"]}',
                        label_visibility='collapsed',
                    )
                    if new_name != parent['name']:
                        db.update_category(parent['id'], name=new_name)
                        st.rerun()
                with cols[3]:
                    if st.button('🗑️', key=f'del_parent_{parent["id"]}', help='删除此大类和其下所有小类'):
                        db.delete_category(parent['id'])
                        st.warning(f'已删除 {parent["name"]} 及其所有子分类')
                        st.rerun()

                # 显示二级分类
                if sub_cats:
                    for sub in sub_cats:
                        scols = st.columns([1, 3, 2, 1, 1])
                        with scols[0]:
                            pass  # 缩进占位
                        with scols[1]:
                            st.text(f'└ {sub["name"]}')
                        with scols[2]:
                            sub_new_name = st.text_input(
                                '改名',
                                value=sub['name'],
                                key=f'edit_sub_{sub["id"]}',
                                label_visibility='collapsed',
                            )
                            if sub_new_name != sub['name']:
                                db.update_category(sub['id'], name=sub_new_name)
                                st.rerun()
                        with scols[3]:
                            pass
                        with scols[4]:
                            if st.button('🗑️', key=f'del_sub_{sub["id"]}', help='删除此小类'):
                                db.delete_category(sub['id'])
                                st.rerun()

                # 在该大类下添加二级分类
                with st.expander(f'➕ 在「{parent["name"]}」下添加二级分类'):
                    new_sub_name = st.text_input(
                        '二级分类名称',
                        placeholder='例如：宵夜',
                        key=f'new_sub_{parent["id"]}',
                    )
                    if st.button('添加', key=f'add_sub_{parent["id"]}'):
                        if new_sub_name.strip():
                            db.add_category(new_sub_name.strip(), 'expense', parent_id=parent['id'])
                            st.success(f'✅ 已添加: {new_sub_name}')
                            st.rerun()
                        else:
                            st.error('⚠️ 请输入分类名称')

                st.divider()

# -------- 收入分类管理 --------
with tab2:
    st.subheader('收入分类（一级）')

    income_cats = db.get_parent_categories('income')

    # 添加新收入分类
    with st.expander('➕ 添加新的收入分类'):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_income_name = st.text_input('分类名称', placeholder='例如：兼职收入', key='new_income_name')
        with col2:
            new_income_icon = st.text_input('图标', placeholder='💻', max_chars=2, key='new_income_icon')
        if st.button('添加收入分类', key='add_income'):
            if new_income_name.strip():
                db.add_category(new_income_name.strip(), 'income', parent_id=None, icon=new_income_icon.strip())
                st.success(f'✅ 已添加: {new_income_name}')
                st.rerun()
            else:
                st.error('⚠️ 请输入分类名称')

    st.divider()

    if not income_cats:
        st.info('暂无收入分类')
    else:
        for cat in income_cats:
            cols = st.columns([4, 2, 1])
            with cols[0]:
                st.markdown(f'### {cat["icon"]} {cat["name"]}')
            with cols[1]:
                new_name = st.text_input(
                    '改名',
                    value=cat['name'],
                    key=f'edit_income_{cat["id"]}',
                    label_visibility='collapsed',
                )
                if new_name != cat['name']:
                    db.update_category(cat['id'], name=new_name)
                    st.rerun()
            with cols[2]:
                if st.button('🗑️', key=f'del_income_{cat["id"]}', help='删除此分类'):
                    db.delete_category(cat['id'])
                    st.warning(f'已删除 {cat["name"]}')
                    st.rerun()
            st.divider()
