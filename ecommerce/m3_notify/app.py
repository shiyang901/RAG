from fastapi import FastAPI
import asyncio, time
from qwen_client import call_qwen_api
from perf_metrics import PerfMetrics

app = FastAPI()
metrics = PerfMetrics("M3 通知用户")

@app.post("/process")
async def process_notify(order_id: int):
    start = time.time()
    result = await call_qwen_api(f"M3 notify user {order_id}")
    await asyncio.sleep(0.03)  # 模拟业务逻辑耗时
    end = time.time()
    metrics.record(start, end)
    return {"status": "user_notified", "order_id": order_id, "detail": result}

@app.get("/metrics")
def get_metrics():
    return {"report": metrics.summary()}
