import asyncio
import time


async def count(t):
    print(f"Started on {t}")
    await asyncio.sleep(t)
    print(f"Ended in {t}")


async def main():
    await asyncio.gather(count(1), count(2), count(3))


if __name__ == '__main__':
    t = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - t
    print(f"Took {elapsed:0.2f} seconds.")
