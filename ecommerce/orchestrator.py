import asyncio
import aiohttp
import time
from perf_metrics import PerfMetrics
from qwen_client import call_qwen_api

# Windows 下使用 SelectorEventLoop 避免 ServerDisconnectedError
import sys
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 模拟微服务调用
async def call_m1(session, order_id):
    async with session.post("http://localhost:8001/process", json={"order_id": order_id}) as resp:
        return await resp.json()

async def call_m2(session, order_id):
    async with session.post("http://localhost:8002/process", json={"order_id": order_id}) as resp:
        return await resp.json()

async def call_m3(session, order_id):
    async with session.post("http://localhost:8003/process", json={"order_id": order_id}) as resp:
        return await resp.json()
# 定义处理单个订单的异步函数，接收会话、订单ID和四个性能监控对象
async def handle_order(session, order_id, metrics_m1, metrics_m2, metrics_m3, metrics_overall):
    start_total = time.time()

    # M1
    start = time.time()
    m1 = await call_m1(session, order_id)
    end = time.time()
    metrics_m1.record(start, end)

    # M2
    start = time.time()
    m2 = await call_m2(session, order_id)
    end = time.time()
    metrics_m2.record(start, end)

    # M3
    start = time.time()
    m3 = await call_m3(session, order_id)
    end = time.time()
    metrics_m3.record(start, end)

    end_total = time.time()
    metrics_overall.record(start_total, end_total)

    return m1, m2, m3

async def run(concurrent_users=100):
    metrics_m1 = PerfMetrics("M1 验证订单")
    metrics_m2 = PerfMetrics("M2 扣减库存")
    metrics_m3 = PerfMetrics("M3 通知用户")
    metrics_overall = PerfMetrics("Overall")

    async with aiohttp.ClientSession() as session:
        tasks = [handle_order(session, order_id, metrics_m1, metrics_m2, metrics_m3, metrics_overall)
                 for order_id in range(1, concurrent_users + 1)]
        start = time.time()
        await asyncio.gather(*tasks)
        end = time.time()

    print("================ 系统总性能 ================")
    print(f"总耗时 ({concurrent_users} 并发用户完成): {end - start:.2f} 秒")
    print(metrics_m1.summary())
    print(metrics_m2.summary())
    print(metrics_m3.summary())
    print(metrics_overall.summary())

if __name__ == "__main__":
    # 并发用户数可以调小，避免真实 Qwen API 调用过多
    asyncio.run(run(concurrent_users=1000))
