from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "deepseek-ai/deepseek-llm-1.3b-base"
save_path = "./models/deepseek-1.3b"

# 强制使用 CPU
device = torch.device("cpu")

print(f"🔄 Downloading model {model_name} to {save_path}...")

# 下载并保存模型权重
model = AutoModelForCausalLM.from_pretrained(model_name, device_map=None)
model.to(device)
model.save_pretrained(save_path)

# 下载并保存 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_path)

print("✅ Done! Model and tokenizer saved to", save_path)