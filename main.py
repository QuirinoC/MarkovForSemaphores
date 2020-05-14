from car import Car
from map import Map
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def main():
  for i in range(5):
    x = asyncio.create_task(Car().vroom({}))

  await x

asyncio.run(main())