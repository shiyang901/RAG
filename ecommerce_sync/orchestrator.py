import time
import requests
from perf_metrics import PerfMetrics
from concurrent.futures import ThreadPoolExecutor, as_completed

# 同步调用各模块
def call_m1(order_id):
    resp = requests.post("http://localhost:8001/process", json={"order_id": order_id})
    return resp.json()

def call_m2(order_id):
    resp = requests.post("http://localhost:8002/process", json={"order_id": order_id})
    return resp.json()

def call_m3(order_id):
    resp = requests.post("http://localhost:8003/process", json={"order_id": order_id})
    return resp.json()

# 处理单个订单
def handle_order(order_id, metrics_m1, metrics_m2, metrics_m3, metrics_overall):
    start_total = time.time()

    # M1 顺序执行
    start = time.time()
    m1 = call_m1(order_id)
    end = time.time()
    metrics_m1.record(start, end)

    # M2 和 M3 并发执行
    with ThreadPoolExecutor(max_workers=2) as executor:
        start_m2 = start_m3 = time.time()
       
        future_m2 = executor.submit(call_m2, order_id)
        future_m3 = executor.submit(call_m3, order_id)
        for future in as_completed([future_m2, future_m3]):
            result = future.result()
            if future == future_m2:
                metrics_m2.record(start_m2, time.time())
                m2 = result
            else:
                metrics_m3.record(start_m3, time.time())
                m3 = result

    end_total = time.time()
    metrics_overall.record(start_total, end_total)
    return m1, m2, m3

# 主程序
def run(total_orders=100):
    metrics_m1 = PerfMetrics("M1 验证订单")
    metrics_m2 = PerfMetrics("M2 扣减库存")
    metrics_m3 = PerfMetrics("M3 通知用户")
    metrics_overall = PerfMetrics("Overall")

    start = time.time()
    for order_id in range(1, total_orders + 1):
        handle_order(order_id, metrics_m1, metrics_m2, metrics_m3, metrics_overall)
    end = time.time()

    print("================ 系统总性能 ================")
    print(f"总耗时 ({total_orders} 用户顺序完成): {end - start:.2f} 秒")
    print(metrics_m1.summary())
    print(metrics_m2.summary())
    print(metrics_m3.summary())
    print(metrics_overall.summary())

if __name__ == "__main__":
    run(total_orders=1000)
