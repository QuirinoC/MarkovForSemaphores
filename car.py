from random import choice
import asyncio
from random import random, randint
from time import sleep

car_colors = ['🚖', '🚘', '🚙', '🚍']
dir_options = ['up', 'down', 'left', 'right']
street_options = list(range(12))


class Car:
    def __init__(self,
                 i,
                 j,
                 map,
                 graph,
                 speed=1,
                 color=None,
                 street=None,
                 ):

        self.i      = i
        self.j      = j
        self.map    = map
        self.graph  = graph
        self.speed  = randint(1, 5) if speed is None else speed
        self.color  = choice(car_colors) if color is None else car_colors[color]
        # The state in the MM
        self.street = choice(street_options) if street is None else street
        self.run    = True
        self.f      = open("log.txt", "w")
        self.lock   = asyncio.Lock()

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'{self.color} ({self.i},{self.j})'

    def move(self, dir):
        dir_map = {
            'up':    (-1, 0),
            'down':  (1, 0),
            'left':  (0, -1),
            'right': (0, 1),
        }
        i, j = dir_map[dir]
        self.i += i
        self.j += j

    async def drive(self):

        symbol_mapper = {
                '^' : 'up',
                'v' : 'down',
                '<' : 'left',
                '>' : 'right'
        }

        while self.run:
            # Get the symbol the car is at
            symbol = self.map[self.i][self.j]
            direction = symbol_mapper.get(symbol)
            if direction:
                self.move(direction)
            else:
                self.run = False
            await asyncio.sleep(1)
