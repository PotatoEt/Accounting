# 💰 Accounting - 个人记账助手

一个基于 [Streamlit](https://streamlit.io) 构建的轻量级个人记账应用，支持**支出 / 收入**双轨记录、**二级分类**管理、**月度统计**和**预算管控**。

> 🎯 专为 Ubuntu 桌面用户设计，一键启动，零配置。

---

## ✨ 功能一览

| 模块 | 说明 |
|------|------|
| 📝 **记账** | 记录支出 / 收入，支持一级大类 → 二级小类的级联选择 |
| 📋 **流水** | 按类型、日期筛选交易记录，查看收支汇总，支持逐条删除 |
| 📊 **统计** | 月度可视化报表：分类饼图、每日趋势折线图、排行榜柱状图 |
| 💰 **预算** | 为支出分类设置月度预算，仪表盘展示执行进度，超支预警 |
| ⚙️ **设置** | 自定义分类（增删改），支出支持二级、收入为一级 |

### 内置分类

| 类型 | 一级分类 | 二级分类数 |
|------|----------|:--------:|
| 支出 | 餐饮、交通、购物、住房、娱乐、医疗、教育、人情、通讯、其他 | 45 个 |
| 收入 | 工资、奖金、兼职、投资、红包、报销、其他 | 7 个 |

---

## 🖥️ 界面预览

- **侧边栏导航** — 所有功能一键触达，底部提供安全关闭按钮
- **响应式布局** — 宽屏自动适配，数据卡片 + 图表同屏展示
- **交互式图表** — Plotly 驱动，悬停显示详情，支持缩放下载
- **实时提示** — 操作成功 / 失败即时反馈，超支红色高亮警示

---

## 🚀 快速开始

### 环境要求

- **Ubuntu** 20.04+（或其他 Linux 发行版）
- **Python** 3.10+
- 无需安装数据库（SQLite 内建）

### 一键启动

```bash
./run.sh
```

脚本会自动完成：
1. 检查 Python 环境
2. 创建虚拟环境（如不存在）
3. 安装依赖
4. 启动应用 → 浏览器打开 `http://localhost:8501`

### 关闭应用

- **网页内关闭**：侧边栏 → 底部"🛑 关闭应用"按钮
- **终端关闭**：`./stop.sh`
- **手动关闭**：在启动终端按 `Ctrl + C`

---

## 📁 项目结构

```
Accounting/
├── app.py                  # 主入口 & 侧边栏导航
├── database.py             # SQLite 数据库层（建表、CRUD、统计查询）
├── run.sh                  # 一键启动脚本
├── stop.sh                 # 进程关闭脚本
├── requirements.txt        # Python 依赖声明
├── coplite.md              # 产品文档（需求 & 设计说明）
│
├── pages/                  # Streamlit 多页面
│   ├── 1_📝_记账.py        # 添加收支记录
│   ├── 2_📋_流水.py        # 交易列表 & 筛选
│   ├── 3_📊_统计.py        # 月度可视化报表
│   ├── 4_💰_预算.py        # 预算设置 & 监控
│   └── 5_⚙️_设置.py       # 分类管理
│
├── utils/                  # 工具模块
│   ├── charts.py           # Plotly 图表生成器
│   └── helpers.py          # 金额 / 日期格式化
│
└── data/                   # 运行时数据（自动创建）
    └── accounting.db       # SQLite 数据库文件
```

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| [Streamlit](https://streamlit.io) | Web 应用框架 |
| [Plotly](https://plotly.com/python/) | 交互式图表 |
| [Pandas](https://pandas.pydata.org) | 数据处理 |
| [SQLite](https://sqlite.org) | 本地数据库（零配置） |
| [openpyxl](https://openpyxl.readthedocs.io) | Excel 导出支持 |

---

## ❓ 常见问题

<details>
<summary><b>启动报 "No module named 'streamlit'"</b></summary>

手动执行以下步骤：
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
</details>

<details>
<summary><b>端口 8501 被占用</b></summary>

指定其他端口启动：
```bash
streamlit run app.py --server.port 8502
```
</details>

<details>
<summary><b>数据文件在哪里？</b></summary>

所有记账数据保存在 `data/accounting.db`（SQLite 数据库）。备份该文件即可备份全部数据。
</details>

<details>
<summary><b>笔记本 / 台式机通用吗？</b></summary>

是的，只要是 Ubuntu 系统（或其他 Linux 发行版），安装 Python 3.10+ 即可运行。
</details>

---

## 📄 License

MIT — 自由使用、修改、分发。
