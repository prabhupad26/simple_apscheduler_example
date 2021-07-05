import asyncio
import time
import random

c = (
    "\033[0m",  # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def markrandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated markrandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"markrandom({idx}) too low, retrying")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"Finished markrandom({idx}).")
    return i


async def main():
    res = await asyncio.gather(*(markrandom(i, 10 - i - 1) for i in range(3)))
    return res


if __name__ == '__main__':
    random.seed(444)
    s = time.perf_counter()
    r1, r2, r3 = asyncio.run(main())
    print(f"r1 : {r1}, r2 : {r2}, r3 : {r3}")
    time_elapsed = time.perf_counter() - s
    print(f"{__file__}Took {time_elapsed:0.2f} seconds")
