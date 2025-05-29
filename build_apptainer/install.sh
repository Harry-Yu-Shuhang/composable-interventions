#!/bin/bash
set -e

echo "📦 激活 Conda 环境..."
source /opt/conda/etc/profile.d/conda.sh
conda activate qwen-compression

export TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6;8.9"

echo "📦 安装 PyTorch..."
pip install --no-cache-dir torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 \
    --index-url https://download.pytorch.org/whl/cu118

echo "📦 升级 pip 工具链..."
pip install -U pip setuptools wheel

echo "📦 安装主项目及依赖（从 pyproject.toml 控制版本）..."
pip install --no-cache-dir --use-pep517 -e /opt/app/

echo "📦 安装 AutoGPTQ（避免build-isolation）..."
pip install --no-build-isolation -e /opt/app/AutoGPTQ

echo "📦 安装 AutoAWQ（可选）..."
pip install --no-build-isolation -e /opt/app/AutoAWQ 