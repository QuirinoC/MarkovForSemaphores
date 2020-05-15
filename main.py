from car import Car
from map import Map
from graph import Graph
from random import randint, random
import asyncio

# Markov graph path
GRAPH_PATH = 'graph.txt'
MAP_PATH = 'mapa_symbols.txt'


async def block():
    # Block for ever
    while True:
        await asyncio.sleep(0xFFFFFFFFFFFF)


async def main():
    zapopan_graph = Graph(GRAPH_PATH)
    zapopan_map = Map(MAP_PATH)

    await zapopan_map.run()


if __name__ == "__main__":
    asyncio.run(main())
