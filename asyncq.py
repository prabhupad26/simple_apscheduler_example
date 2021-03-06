import asyncio
import argparse
import os
import random
import itertools as it
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds")
    await asyncio.sleep(i)


async def consumer(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}> "
              f"in {now - t:0.5f} seconds. ")
        q.task_done()


async def producer(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    print(f"Producer {name} will add <{n}> times")
    for _ in it.repeat(None, n):
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(producer(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consumer(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--nprod', type=int, default=2)
    parser.add_argument('-c', '--ncon', type=int, default=5)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
