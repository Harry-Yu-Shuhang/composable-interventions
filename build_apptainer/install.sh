#!/bin/bash
set -e

echo "📦 激活 Conda 环境..."
source /opt/conda/etc/profile.d/conda.sh
conda activate lm-compose

echo "📦 安装 PyTorch..."
pip install --no-cache-dir torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 \
    --index-url https://download.pytorch.org/whl/cu118

echo "📦 安装 Python 基础依赖..."
pip install -U pip setuptools wheel
pip install pandas numpy huggingface_hub[cli] transformers accelerate gekko packaging==24.0

echo "📦 安装主项目..."
pip install --use-pep517 -e /opt/app/

echo "📦 安装 AutoGPTQ..."
pip install --no-build-isolation /opt/app/AutoGPTQ