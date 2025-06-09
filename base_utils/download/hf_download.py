from huggingface_hub import snapshot_download, hf_hub_download  # 一个整个下载，一个可以指定局部下载
from pathlib import Path

# 从镜像网站下载模型
model_id = "sand-ai/MAGI-1"
local_dir = "/media/pan/新加卷/checkpoints/"
dir_name = Path(model_id).stem
print(dir_name)
snapshot_download(model_id, local_dir=f"{local_dir}/{dir_name}",
                  local_dir_use_symlinks=False,
                  revision="main",
                #   endpoint="https://hf-mirror.com",
                  allow_patterns=["ckpt/magi/24B_distill_quant/inference_weight.fp8.distill/*"],
                  resume_download=True)

# hf_hub_download(model_id, filename="model-00001-of-00003.safetensors", 
#                 subfolder="ckpt/magi/24B_distill_quant/inference_weight.fp8.distill",
#                 local_dir=f"./{dir_name}",
#                 endpoint="https://hf-mirror.com",)

