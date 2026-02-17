#!/bin/bash

echo "======================================"
echo "  徒步活动组织系统 - 启动脚本"
echo "======================================"
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查是否安装了依赖
echo ""
echo "检查依赖包..."
if python3 -c "import streamlit" 2>/dev/null; then
    echo "✓ Streamlit 已安装"
else
    echo "✗ Streamlit 未安装，正在安装..."
    pip3 install -r requirements.txt
fi

# 创建必要的目录
echo ""
echo "创建必要的目录..."
mkdir -p data assets

echo ""
echo "======================================"
echo "  启动应用..."
echo "======================================"
echo ""

# 启动Streamlit应用
streamlit run app.py
