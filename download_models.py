from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "deepseek-ai/deepseek-llm-1.3b-base"
save_path = "./models/deepseek-1.3b"

model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(save_path)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_path)