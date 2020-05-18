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
                 street,
                 next_street,
                 speed=1,
                 color=None,

                 ):

        self.i      = i
        self.j      = j
        self.map    = map
        self.graph  = graph
        self.locks  = locks
        self.speed  = randint(1, 5) if speed is None else speed
        self.color  = choice(car_colors) if color is None else car_colors[color]
        # The state in the MM
        self.street = street
        self.next_street = next_street
        self.run    = True
        self.lock   = asyncio.Lock()
        self.prev_lock = None

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'{self.color} ({self.i},{self.j} {self.street}->{self.next_street})'

    def validate_coord(self, i, j):
        return \
                i >= 0 and\
                i <  len(self.locks) and\
                j >=0 and\
                j <  len(self.locks[0])

    async def move_next(self, direction):
        # Get next spot for car
        i, j = self.get_next(direction)
        is_valid_pos = self.validate_coord(i,j)
        # Avoid trying to lock a Lock out of bounds
        if is_valid_pos:
            await self.locks[i][j].acquire()
        # Move the car anyways so the matrix can kill it
        self.i = i
        self.j = j
        if self.prev_lock and self.prev_lock.locked(): 
            self.prev_lock.release()
            # Release prev_lock for next car
        
        if is_valid_pos:
            self.prev_lock = self.locks[i][j]
        
        # End car loop if it is stopped
        if not is_valid_pos:
            self.run = False

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
            await asyncio.sleep(0.5)
            # Get the symbol the car is at
            symbol = self.map[self.i][self.j]
            direction = symbol_mapper.get(symbol)
            if direction:
                await self.move_next(direction)       
                prev_direction = direction        
            elif symbol == '+':
                self.move = False
            else:
                # Time to make a turn
                self.street = self.next_street
                self.next_street = self.graph.decide(self.street)
                await self.move_next(prev_direction)
