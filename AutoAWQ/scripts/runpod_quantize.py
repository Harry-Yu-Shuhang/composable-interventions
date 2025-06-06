import os
import time
import runpod

# Load environment variables
HF_TOKEN = os.environ.get('HF_TOKEN')
runpod.api_key = os.environ.get('RUNPOD_API_KEY')

# RunPod Parameters
# get more by running print(runpod.get_gpus())
template_name = f"AutoAWQ Pod {int(time.time())}"
docker_image = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
gpu_ids = {
    "MI300X": "AMD Instinct MI300X OAM",
    "B200": "NVIDIA B200",
    "H200": "NVIDIA H200",
    "H100": "NVIDIA H100 80GB HBM3",
    "A100": "NVIDIA A100-SXM4-80GB",
    "A6000": "NVIDIA RTX A6000",
    "4090": "NVIDIA GeForce RTX 4090",
}
env_variables = {
    "HF_TOKEN": HF_TOKEN,
}
gpu_id = gpu_ids["H200"]
num_gpus = 1
system_memory_gb = 100
system_storage_gb = 300 # fp16 model is downloaded here
volume_storage_gb = 100 # quantized model is saved here

# Quantization Parameters
hf_model_path = "meta-llama/Llama-3.2-3B-Instruct"
quant_name = "Llama-3.2-3B-Instruct-awq".lower()
local_save_path = f"/workspace/{quant_name}"
hf_upload_path = f"casperhansen/{quant_name}"
INSTALL_TRANSFORMERS_MAIN = False
USE_HF_TRANSFER = True

if USE_HF_TRANSFER:
    env_variables["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

cli_args = dict(
    hf_model_path = hf_model_path,
    quant_name = quant_name,
    local_save_path = local_save_path,
    zero_point = True,
    q_group_size = 128,
    w_bit = 4,
    version = "GEMM",
)
cli_args = " ".join([f"--{k}" if isinstance(v, bool) else f"--{k} {v}" for k,v in cli_args.items()])

commands = [
    "cd /workspace",
    "pip install requests",
    "git clone https://github.com/casper-hansen/AutoAWQ.git",
    "cd AutoAWQ",
    "pip install -e .",
    "pip install -U git+https://github.com/huggingface/transformers.git" if INSTALL_TRANSFORMERS_MAIN else "",
    "pip install hf-transfer" if USE_HF_TRANSFER else "",
    "huggingface-cli login --token $HF_TOKEN",
    f"python examples/cli.py {cli_args}",
    f"huggingface-cli upload {hf_upload_path} {local_save_path} ./",
    "runpodctl stop pod $RUNPOD_POD_ID",
]
commands = [cmd for cmd in commands if cmd]
commands = " && ".join(commands)

docker_command = "bash -c '" + commands + "'"

template = runpod.create_template(
    name=template_name,
    image_name=docker_image,
    docker_start_cmd=docker_command,
    container_disk_in_gb=system_storage_gb,
    volume_in_gb=volume_storage_gb,
    volume_mount_path="/workspace",
    ports="8888/http,22/tcp",
)

pod = runpod.create_pod(
    name=template_name,
    image_name=docker_image,
    template_id=template["id"],
    gpu_type_id=gpu_id,
    gpu_count=num_gpus,
    min_memory_in_gb=system_memory_gb,
    volume_in_gb=volume_storage_gb,
    container_disk_in_gb=system_storage_gb,
    env=env_variables,
    volume_mount_path="/workspace",
    cloud_type="SECURE",
)

print(pod)
