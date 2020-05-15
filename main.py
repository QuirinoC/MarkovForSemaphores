from car import Car
from map import Map
from graph import Graph
from random import randint, random
import asyncio

async def block():
  # Block for ever
  while True:
    await asyncio.sleep(0xFFFFFFFFFFFF)

async def main():
  car_map = {}
  map = Map('mapa_symbols.txt', car_map)
  car_map[0] = Car(15, 10, graph)
  car_map[1] = Car(15, 11, graph)

  for i in car_map:
    asyncio.create_task(car_map[i].vroom())
  asyncio.create_task(map.render_map())


  await block()

if __name__ == "__main__":
  asyncio.run(main())