import os
import requests

API_KEY = os.getenv("sk-800d5301c0ff4f9cb377c65093468ba3")

def call_qwen_api(prompt: str):
    """
    同步调用 Qwen API
    """
    url = "https://api.qwen.com/v1/generation"  # 替换成真实 Bench API
    headers = {"Authorization": f"Bearer {API_KEY}"}
    json_data = {"prompt": prompt, "model": "qwen-plus"}

    resp = requests.post(url, headers=headers, json=json_data)
    if resp.status_code == 200:
        return resp.json().get("output", {}).get("text", "")
    else:
        return f"Error: {resp.text}"
