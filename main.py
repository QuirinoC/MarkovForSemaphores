from car import Car
from map import Map
from graph import Graph
from random import randint
import asyncio

async def block():
  # Block for ever
  while True:
    await asyncio.sleep(0xFFFFFFFFFFFF)

async def main():
  car_map = {}
  map = Map('mapa_4_X.txt', car_map)
  graph = [
            # L    R    F    U
            [0.2, 0.49, 0.3, 0.01], #A
            [0.25, 0.15, 0.5, 0.1], #B
            [0.4, 0.3, 0.3, 0.0],   #C
            [0.25, 0.15, 0.5, 0.1]  #D
        ]
  car_map[0] = Car(15, 10, graph)

  asyncio.create_task(car_map[0].vroom())
  asyncio.create_task(map.render_map())


  await block()

if __name__ == "__main__":
  
  asyncio.run(main())