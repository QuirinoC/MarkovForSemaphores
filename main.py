from car import Car
from map import Map
from random import randint
import asyncio

async def block():
  # Block for ever
  while True:
    await asyncio.sleep(0xFFFFFFFFFFFF)

async def main():
  car_map = {}
  map = Map('mapa_4.txt', car_map)
  car_map[0] = Car(15,0)

  asyncio.create_task(car_map[0].vroom())
  asyncio.create_task(map.render_map())


  await block()

if __name__ == "__main__":
  
  asyncio.run(main())