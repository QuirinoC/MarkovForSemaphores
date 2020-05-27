from car import Car
from map import Map
from graph import Graph
from random import randint, random
import asyncio

import argparse

parser = argparse.ArgumentParser(description='Run a small city')
parser.add_argument('--gui', dest='gui', action='store_true')
parser.add_argument('--right', dest='right', action='store_true')
parser.add_argument('speed', metavar='speed', type=int)
parser.add_argument('ncars', metavar='ncars', type=int)
parser.add_argument('state', metavar='state', type=int)
args = parser.parse_args()

GUI = args.gui
SPEED = 1 / args.speed
N_CARS = args.ncars
RIGHT_TURN = args.right
STATE = args.state

# Markov graph path
GRAPH_PATH = 'graph.txt'
MAP_PATH = 'mapa_symbols.txt'

async def block():
    # Block for ever
    while True:
        await asyncio.sleep(0xFFFFFFFFFFFF)


async def main():
    zapopan_graph = Graph(GRAPH_PATH)
    zapopan_map = Map(MAP_PATH, zapopan_graph, SPEED, N_CARS, {}, GUI, RIGHT_TURN, STATE)

    await zapopan_map.run()
    

if __name__ == "__main__":
    asyncio.run(main())