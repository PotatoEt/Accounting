#!/bin/bash
# ============================================
# Accounting - 一键启动脚本
# 用法: ./run.sh
# ============================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  💰 Accounting - 个人记账应用"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python"
    echo "   Ubuntu 安装命令: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# 绕过代理（系统代理不可用时避免网络问题）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# 如果虚拟环境不存在，自动创建
if [ ! -d ".venv" ]; then
    echo "📦 正在创建虚拟环境..."
    python3 -m venv .venv 2>/dev/null || {
        python3 -m venv --without-pip .venv
        curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
    }
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "📦 正在检查依赖..."
pip install -q -r requirements.txt

echo ""
echo "🚀 正在启动应用..."
echo "   浏览器将自动打开，如未打开请手动访问: http://localhost:8501"
echo "   按 Ctrl+C 可以停止应用"
echo ""

# 启动 Streamlit
streamlit run app.py --server.headless true --server.port 8501
