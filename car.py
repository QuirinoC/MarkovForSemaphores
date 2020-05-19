from random import choice
import asyncio
from random import random, randint
from time import sleep
import numpy as np

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

    def move_to_lockless(self, i, j):
        '''
            This is a workaround lmao
        '''
        # Move to a specific i,j coord
        is_valid_pos = self.validate_coord(i, j)

        # Move the car anyways so the matrix can kill it
        self.i = i
        self.j = j

        # Leave the prev lock
        if self.prev_lock and self.prev_lock.locked():
            self.prev_lock.release()

        

    def get_next(self, dir):
        dir_map = {
            'up':    (-1, 0),
            'down':  (1, 0),
            'left':  (0, -1),
            'right': (0, 1),
        }
        i, j = dir_map[dir]
        return (self.i + i), (self.j + j)

    def distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return (
            (x2 - x1) ** 2 +\
            (y2 - y1) ** 2
        ) ** 0.5

    def get_points(self, p1, p2):
        parts = self.distance(p1,p2)
        points =  list(
            zip(
                [int(round(i)) for i in np.linspace(p1[0], p2[0], parts+parts)],
                [int(round(j)) for j in np.linspace(p1[1], p2[1], parts+parts)]
            )
        )
        seen = set()
        seen_add = seen.add
        return [x for x in points if not (x in seen or seen_add(x))]

    async def turn(self, target_i, target_j):
        for i, j in self.get_points((self.i, self.j), (target_i, target_j))[1:]:
            self.move_to_lockless(i,j)
            await asyncio.sleep(0.5)

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
