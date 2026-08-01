"""
图表生成模块
使用 Plotly 生成饼图、折线图、柱状图等交互式图表。
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# 统一的图表颜色配置
COLORS = px.colors.qualitative.Set3


def create_category_pie(cat_summary, title='消费分类占比'):
    """
    生成分类占比饼图
    cat_summary: [{'name': '餐饮', 'icon': '🍜', 'total': 520.5}, ...]
    """
    if not cat_summary:
        return None

    df = pd.DataFrame(cat_summary)
    df['label'] = df.apply(lambda r: f"{r.get('icon', '')} {r['name']}", axis=1)

    fig = px.pie(
        df,
        values='total',
        names='label',
        title=title,
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}<br>金额: ¥%{value:,.2f}<extra></extra>',
    )
    fig.update_layout(
        height=450,
        margin=dict(t=60, b=20, l=20, r=20),
    )
    return fig


def create_daily_line(daily_summary, title='每日支出趋势'):
    """
    生成每日趋势折线图
    daily_summary: [{'date': '2026-08-01', 'total': 35.5}, ...]
    """
    if not daily_summary:
        return None

    df = pd.DataFrame(daily_summary)
    df['date'] = pd.to_datetime(df['date'])

    fig = px.line(
        df,
        x='date',
        y='total',
        title=title,
        markers=True,
    )
    fig.update_traces(
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=8),
        hovertemplate='日期: %{x|%m月%d日}<br>金额: ¥%{y:,.2f}<extra></extra>',
    )
    fig.update_layout(
        height=350,
        margin=dict(t=60, b=20, l=20, r=20),
        xaxis_title='',
        yaxis_title='金额（元）',
    )
    return fig


def create_category_bar(cat_summary, title='分类消费排行'):
    """
    生成分类排行柱状图
    """
    if not cat_summary:
        return None

    df = pd.DataFrame(cat_summary)
    df['label'] = df.apply(lambda r: f"{r.get('icon', '')} {r['name']}", axis=1)
    df = df.sort_values('total')

    fig = px.bar(
        df,
        x='total',
        y='label',
        title=title,
        orientation='h',
        color='total',
        color_continuous_scale='Reds',
        text_auto='.2f',
    )
    fig.update_traces(
        hovertemplate='%{y}<br>金额: ¥%{x:,.2f}<extra></extra>',
    )
    fig.update_layout(
        height=400,
        margin=dict(t=60, b=20, l=20, r=20),
        xaxis_title='金额（元）',
        yaxis_title='',
        coloraxis_showscale=False,
    )
    return fig


def create_budget_gauge(spent, budget, title='预算使用情况'):
    """
    生成预算仪表盘（进度条风格的仪表图）
    spent: 已花金额
    budget: 预算金额
    """
    if budget <= 0:
        return None

    percent = min(spent / budget * 100, 100)
    remaining = max(budget - spent, 0)

    # 根据百分比选择颜色
    if percent >= 100:
        color = '#FF4444'  # 超预算红色
        status = '⚠️ 已超预算！'
    elif percent >= 80:
        color = '#FFA726'  # 接近预算橙色
        status = '⚡ 快要超预算了'
    else:
        color = '#66BB6A'  # 正常绿色
        status = '✅ 预算充足'

    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=spent,
        delta={'reference': budget, 'decreasing': {'color': 'green'}},
        number={'prefix': '¥', 'valueformat': ',.2f'},
        title={'text': f'{title}<br><span style="font-size:14px">{status}</span>'},
        gauge={
            'axis': {'range': [0, budget], 'tickprefix': '¥'},
            'bar': {'color': color},
            'steps': [
                {'range': [0, budget * 0.6], 'color': '#E8F5E9'},
                {'range': [budget * 0.6, budget * 0.8], 'color': '#FFF3E0'},
                {'range': [budget * 0.8, budget], 'color': '#FFEBEE'},
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 3},
                'thickness': 0.8,
                'value': budget,
            },
        },
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=80, b=20, l=40, r=40),
    )
    return fig
