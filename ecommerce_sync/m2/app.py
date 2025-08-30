from fastapi import FastAPI
import time
from qwen_client import call_qwen_api
from perf_metrics import PerfMetrics

app = FastAPI()
metrics = PerfMetrics("M2 扣减库存")

@app.post("/process")
def process_inventory(order_id: int):
    start = time.time()
    result = call_qwen_api(f"M2 deduct inventory {order_id}")
    time.sleep(0.07)  # 模拟业务逻辑耗时
    end = time.time()
    metrics.record(start, end)
    return {"status": "inventory_deducted", "order_id": order_id, "detail": result}

@app.get("/metrics")
def get_metrics():
    return {"report": metrics.summary()}
