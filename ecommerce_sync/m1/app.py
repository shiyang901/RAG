from fastapi import FastAPI
import time
from qwen_client import call_qwen_api
from perf_metrics import PerfMetrics
import time

app = FastAPI()
metrics = PerfMetrics("M1 验证订单")

@app.post("/process")
def process_order(order_id: int):
    """
    同步处理订单验证
    """
    start = time.time()
    # 同步调用 Qwen API
    result = call_qwen_api(f"M1 validate order {order_id}")
    
    # 模拟业务逻辑耗时（同步）
    time.sleep(0.05)

    end = time.time()
    metrics.record(start, end)

    return {"status": "validated", "order_id": order_id, "detail": result}

@app.get("/metrics")
def get_metrics():
    """
    返回 M1 模块延迟统计报表
    """
    return {"report": metrics.summary()}
