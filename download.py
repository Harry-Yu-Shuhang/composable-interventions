from huggingface_hub import snapshot_download

# 下载 deepseek-math-7b-instruct
snapshot_download(
    repo_id="deepseek-ai/deepseek-math-7b-instruct",
    local_dir="models/deepseek-math-7b-instruct",
    local_dir_use_symlinks=False
)

# 下载 Qwen2.5-32B-Instruct
snapshot_download(
    repo_id="Qwen/Qwen2.5-32B-Instruct",
    local_dir="models/Qwen2.5-32B-Instruct",
    local_dir_use_symlinks=False
)
