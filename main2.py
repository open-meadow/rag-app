import sys
import os

vllm_path = "/Users/open-meadow/Desktop/U-TO/rag-app/.venv/bin/vllm"

sys.path.append(os.path.dirname(vllm_path))

from vllm import LLM, SamplingParams
import torch

use_mps = torch.backends.mps.is_available()
device_type = "mps" if use_mps else "cpu"

print(f"Using device: {device_type}")

llm = LLM(
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    download_dir = "./models",
    tensor_parallel_size = 1,
    trust_remote_code = True,
    dtype = "float16" if use_mps else "float32"
)

sampling_params = SamplingParams(
    temperature = 0.7,
    top_p = 0.95,
    max_tokens = 100
)

prompt = "Write a short poem about artificial intelligence"
outputs = llm.generate([prompt], sampling_params)

for output in outputs:
    print(output.outputs[0].text)