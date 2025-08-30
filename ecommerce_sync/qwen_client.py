
from dashscope import Generation

# 这里需要你设置 API Key
# export DASHSCOPE_API_KEY="你的API Key"
# 或者在代码里写死（不推荐）
import os
API_KEY = os.getenv("sk-800d5301c0ff4f9cb377c65093468ba3")

def _sync_call(prompt: str):
    response = Generation.call(
        model="qwen-plus",   # 你也可以换成 qwen-turbo / qwen-max
        prompt=prompt,
        api_key=API_KEY
    )
    if response.status_code == 200:
        return response.output["text"]
    else:
        return f"Error: {response.message}"