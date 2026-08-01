#!/bin/bash
# ============================================
# Accounting - 关闭应用脚本
# 用法: ./stop.sh
# 说明: 找到并停止正在运行的 Streamlit 进程
# ============================================

# 查找 streamlit 进程
PIDS=$(pgrep -f "streamlit run app.py" 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "❌ 未找到正在运行的 Accounting 应用"
    echo "   如果没有启动过，请先执行 ./run.sh"
    exit 0
fi

echo "🔍 找到以下进程："
for pid in $PIDS; do
    echo "   PID: $pid ($(ps -p $pid -o comm= 2>/dev/null))"
done

echo ""
echo "🛑 正在关闭..."

# 先尝试优雅关闭（SIGTERM）
for pid in $PIDS; do
    kill $pid 2>/dev/null
done

sleep 1

# 检查是否还有残留进程，有就强制关闭
REMAIN=$(pgrep -f "streamlit run app.py" 2>/dev/null)
if [ -n "$REMAIN" ]; then
    echo "   优雅关闭失败，尝试强制关闭..."
    for pid in $REMAIN; do
        kill -9 $pid 2>/dev/null
    done
fi

echo "✅ Accounting 应用已关闭"
echo "   重新启动请执行: ./run.sh"
