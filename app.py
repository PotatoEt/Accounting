"""
Accounting - 个人记账应用 · 主入口
Streamlit 配置 + 侧边栏导航
启动命令: streamlit run app.py
"""

import streamlit as st
import os
import signal

# ============================================================
# 页面配置（必须是第一个 Streamlit 命令）
# ============================================================
st.set_page_config(
    page_title='💰 Accounting - 个人记账',
    page_icon='💰',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ============================================================
# 隐藏 Streamlit 默认样式（让界面更干净）
# ============================================================
hide_style = '''
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
'''
st.markdown(hide_style, unsafe_allow_html=True)

# ============================================================
# 侧边栏导航
# ============================================================
with st.sidebar:
    st.image(
        'https://img.icons8.com/color/96/money-box.png',
        width=64,
    )
    st.title('💰 Accounting')
    st.caption('个人记账助手 v1.0')

    st.divider()

    # Streamlit 的 pages 机制会自动处理导航，
    # 这里只是做个欢迎说明
    st.markdown('''
    ### 📌 快速导航

    左侧菜单选择功能页面：
    - 📝 **记账** — 记录收支
    - 📋 **流水** — 查看记录
    - 📊 **统计** — 图表报表
    - 💰 **预算** — 预算管理
    - ⚙️ **设置** — 分类管理
    ''')

    st.divider()
    st.caption('💡 数据存储在本地 `data/` 文件夹中')
    st.caption('🖥️ 运行环境：Ubuntu + Streamlit')

    st.divider()

    # ---- 关闭应用按钮 ----
    # 用一个折叠区域来防止误触
    with st.expander('🔴 关闭应用', expanded=False):
        st.warning('⚠️ 关闭后需要重新执行 `./run.sh` 才能再次启动')
        if st.button('🛑 确认关闭', type='primary', use_container_width=True):
            st.success('👋 应用已关闭，感谢使用！')
            # 结束 Streamlit 进程
            os.kill(os.getpid(), signal.SIGTERM)

# ============================================================
# 主页面内容
# ============================================================
st.title('👋 欢迎使用 Accounting')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label='📝 今天记账了吗？', value='从记账页开始', delta='')

with col2:
    st.metric(label='📊 想看报表？', value='去统计页查看', delta='')

with col3:
    st.metric(label='💰 设置预算？', value='去预算页管理', delta='')

st.divider()

# 快速开始步骤
st.markdown('''
### 🚀 快速开始

1. **点左侧「📝 记账」** → 开始记录你的第一笔消费或收入
2. **点左侧「📋 流水」** → 查看所有历史记录，可以删除不需要的
3. **点左侧「📊 统计」** → 选择月份，查看消费分析图表
4. **点左侧「💰 预算」** → 设置月度预算，控制开支
5. **点左侧「⚙️ 设置」** → 添加或修改分类

---

### 💡 小提示

- 所有数据都保存在你电脑的 `Accounting/data/` 文件夹里，不用担心数据丢失
- 想备份数据？直接复制 `data/accounting.db` 这个文件就行
- 分类分两级：一级大类（如餐饮）→ 二级小类（如午餐）
- 收入只有一级分类（如工资、奖金等）
''')
