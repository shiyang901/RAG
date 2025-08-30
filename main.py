import asyncio
import time

async def say_after(delay,what):
    await asyncio.sleep(delay)
    return f"{what}-{delay}"


async def main():
    task1 = asyncio.create_task(say_after(1,'hello'))
    task2 = asyncio.create_task(say_after(2,'world'))

    print(f"started at {time.strftime('%X')}")

    """ ret1 = await task1
    ret2 = await task2 """
    ret = await asyncio.gather(task1,task2)

    """ print(ret1)
    print(ret2) """

    print(ret)

    print(f"finished at {time.strftime('%X')}")



coro = main()
asyncio.run(coro)#从synchronize模式变换到asynchronize模式的入口

#将coroutine变成task,排队执行