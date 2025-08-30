import asyncio, aiohttp, time

URL = "http://localhost:8002/process"   # M1 → 8001, M2 → 8002, M3 → 8003
REQUESTS = 500

async def call_service(session, i):
    async with session.post(URL, json={"order_id": i}) as resp:
        return await resp.json()

async def run_benchmark():
    async with aiohttp.ClientSession() as session:
        tasks = [call_service(session, i) for i in range(REQUESTS)]
        start = time.time()
        await asyncio.gather(*tasks)
        end = time.time()
        print(f"模块总耗时: {end-start:.2f}s ({REQUESTS} requests)")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
