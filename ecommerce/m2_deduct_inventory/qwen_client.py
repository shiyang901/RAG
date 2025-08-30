import asyncio
from dashscope import Generation
import os

# 从环境变量获取 API Key
API_KEY = os.getenv("sk-800d5301c0ff4f9cb377c65093468ba3")

async def call_qwen_api(prompt: str):
    """
    异步调用 Qwen API（Bench 异步方式）
    """
    response = await Generation.acall(
        model="qwen-plus",   # 可换 qwen-turbo / qwen-max
        prompt=prompt,
        api_key=API_KEY
    )
    if response.status_code == 200:
        return response.output["text"]
    else:
        return f"Error: {response.message}"


