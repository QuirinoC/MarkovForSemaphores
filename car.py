from random import choice
import asyncio
from random import random, randint
from time import sleep

car_colors = ['🚖', '🚘', '🚍']
dir_options = ['up', 'down', 'left', 'right']
street_options = list(range(12))

class Car:
    def __init__(self,
                 i,
                 j,
                 map,
                 graph,
                 locks,
                 speed=1,
                 color=None,
                 street=None,
                 ):

        self.i      = i
        self.j      = j
        self.map    = map
        self.graph  = graph
        self.locks  = locks
        self.speed  = randint(1, 5) if speed is None else speed
        self.color  = choice(car_colors) if color is None else car_colors[color]
        # The state in the MM
        self.street = choice(street_options) if street is None else street
        self.run    = True
        self.lock   = asyncio.Lock()
        self.prev_lock = None

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'{self.color} ({self.i},{self.j})'

    def validate_coord(self, i, j):
        return \
                i >= 0 and\
                i <  len(self.locks) and\
                j >=0 and\
                j <  len(self.locks[0])

    async def move_next(self, direction):
        # Get next spot for car
        i, j = self.get_next(direction)

        # Avoid cars overlapping by using locks
        await self.locks[i][j].acquire()
        self.i = i
        self.j = j
        if self.prev_lock: 
            self.prev_lock.release()
        # Release prev_lock for next car
        self.prev_lock = self.locks[i][j]

    def get_next(self, dir):
        dir_map = {
            'up':    (-1, 0),
            'down':  (1, 0),
            'left':  (0, -1),
            'right': (0, 1),
        }
        i, j = dir_map[dir]
        return (self.i + i), (self.j + j)

    async def drive(self):

        symbol_mapper = {
                '^' : 'up',
                'v' : 'down',
                '<' : 'left',
                '>' : 'right'
        }
        prev_direction = None
        while self.run:
            # Get the symbol the car is at
            symbol = self.map[self.i][self.j]
            direction = symbol_mapper.get(symbol)
            if direction:
                await self.move_next(direction)       
                prev_direction = direction        
            else:
                await self.move_next(prev_direction)
            await asyncio.sleep(.1)
