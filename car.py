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
                 intersections,
                 speed=1,
                 color=None,

                 ):

        self.i = i
        self.j = j
        self.map = map
        self.graph = graph
        self.locks = locks
        self.speed = randint(1, 5) if speed is None else speed
        self.color = choice(car_colors) if color is None else car_colors[color]
        # The state in the MM
        self.street = street
        self.next_street = next_street
        self.intersections = intersections
        self.run = True
        self.lock = asyncio.Lock()
        self.prev_lock = None

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'{self.color} ({self.i},{self.j} {self.street}->{self.next_street})'

    def validate_coord(self, i, j):
        return \
                i >= 0 and\
                i < len(self.locks) and\
                j >= 0 and\
                j < len(self.locks[0])

    async def move_next(self, direction):
        # Get next spot for car
        i, j = self.get_next(direction)
        await self.move_to(i, j)

    async def move_to(self, i, j):
        # Move to a specific i,j coord
        is_valid_pos = self.validate_coord(i, j)
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

    async def turn_i(self, target_i):
        while self.i != target_i:
            if self.i < target_i:
                await self.move_to(self.i + 1, self.j)
            else:
                    await self.move_to(self.i - 1, self.j)
            await asyncio.sleep(0.5)
        
    async def turn_j(self, target_j):
         while self.j != target_j:
            if self.j < target_j:
                await self.move_to(self.i , self.j + 1)
            else:
                await self.move_to(self.i, self.j - 1)
            await asyncio.sleep(0.5)

    async def turn(self, target_i, target_j):
        turn_i_t =  self.turn_i(target_i)
        turn_j_t =  self.turn_j(target_j)

        if self.prev_direction in 'v^':
            await turn_i_t
            await turn_j_t
        else:
            await turn_j_t
            await turn_i_t

    async def drive(self):

        symbol_mapper = {
                '^' : 'up',
                'v' : 'down',
                '<' : 'left',
                '>' : 'right'
        }
        self.prev_direction = None
        while self.run:
            # Get the symbol the car is at
            symbol = self.map[self.i][self.j]
            direction = symbol_mapper.get(symbol)
            if direction:
                await self.move_next(direction)       
                self.prev_direction = direction        

                await asyncio.sleep(0.5)

            elif symbol == '+':
                self.street = self.next_street
                self.next_street = self.graph.decide(self.street)
                turn_pos = self.intersections[self.street]
                target_i, target_j = choice(turn_pos)

                # Make turn
                await self.turn(target_i,target_j)

            else:
                await self.move_next(self.prev_direction)
