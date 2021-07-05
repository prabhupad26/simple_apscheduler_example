import asyncio
import random
import time


async def part1(n):
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"Returning part1({n}) == {result}")
    return result


async def part2(n, arg):
    i = random.randint(0, 10)
    print(f"part2({n, arg}) sleeping for {i} seconds")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"Returning part2({n, arg}) == {result}")
    return result


async def chain(n):
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    print(f"Chain({n}) => {p2} took {end:0.2f} seconds.")


async def main(*args):
    await asyncio.gather(*(chain(arg) for arg in args))


if __name__ == '__main__':
    t = time.perf_counter()
    random.seed(444)
    inp = [1, 2, 3]
    asyncio.run(main(*inp))
    elapsed = time.perf_counter() - t
    print(f"Took {elapsed:0.2f} seconds.")
