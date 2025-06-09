from modelscope import snapshot_download

target_dir = "/media/pan/新加卷/checkpoints/"

model_dir = snapshot_download('Qwen/Qwen3-Embedding-0.6B', cache_dir=target_dir)