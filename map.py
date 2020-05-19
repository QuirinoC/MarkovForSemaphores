from os import system, name
import asyncio
from car import Car, car_colors
from random import choice
from semaphore import SemaphoreSet
from pprint import pprint

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

cls_cmd = 'clear' if name == 'posix' else 'cls'

SPAWNS = {
    # Spawns from the left side
    'B': {
        'A': (13, 0),  # U Turn
        'D': (13, 0),  # Left turn
        'F': (14, 0),  # Go straight
        'K': (15, 0),  # Right turn
    },
    'P': {
        'O': (29, 0),  # U Turn
        'L': (29, 0),  # Left turn
        'T': (30, 0),  # Go straight
        'Q': (31, 0),  # Right turn
    },
    # Spawns from top
    'C': {
        'D': (0, 23),  # U Turn
        'F': (0, 23),  # Left turn
        'K': (0, 22),  # Go straight
        'A': (0, 21),  # Right turn
    },
    'G': {
        'H': (0, 61),  # U Turn
        'J': (0, 61),  # Left turn
        'M': (0, 60),  # Go straight
        'E': (0, 59),  # Right turn
    },
    # Spawns from the right
    'I': {
        'J': (12, 85),  # U Turn
        'H': (12, 85),  # Left turn
        'E': (11, 85),  # Go straight
        'M': (10, 85),  # Right turn
    },
    'W': {
        'X': (28, 85),  # U Turn
        'U': (28, 85),  # Left turn
        'S': (27, 85),  # Go straight
        'N': (26, 85),  # Right turn
    },
    # Spawns from the bottom
    'R': {
        'Q': (41, 24),  # U Turn
        'O': (41, 24),  # Left turn
        'L': (41, 25),  # Go straight
        'T': (41, 26),  # Right turn
    },
    'V': {
        'U': (41, 62),  # U Turn
        'S': (41, 62),  # Left turn
        'N': (41, 63),  # Go straight
        'X': (41, 64),  # Right turn
    },
}


def clear():
    system(cls_cmd)

class Map:
    def __init__(self, path: str, graph: [[str]], cars: dict = {}):
        self.grid = self.parse_map(path)
        self.intersections = self.load_intersections()
        self.graph = graph
        # Keep track of the cars
        self.cars = cars
        self.locks = [[asyncio.Lock() for j in range(len(self.grid[0]))]
                      for i in range(len(self.grid))]
        self.semaphores = self.load_semaphores()

    def load_intersections(self):
        direction_mapper = {
            # Horizontal
            'A' : '<',
            'F' : '>',
            'E' : '<',
            'J' : '>',
            'O' : '<',
            'T' : '>',
            'S' : '<',
            'X' : '>',
            # Vertical
            'D' : '^',
            'K' : 'v',
            'H' : '^',
            'M' : 'v',
            'L' : '^',
            'Q' : 'v',
            'N' : '^',
            'U' : 'v',

        }
        horizontal = 'AFEJOTSX'
        vertical   = 'DKHMLQNU'
        # Load intersection data and revert grid
        data = {}
        for idx, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col in 'ABCDEFGHIJKLMNOPQRSTUVWX':
                    data[col] = data.get(col, []) + [(idx,j)]
                    self.grid[idx][j] = direction_mapper[col]
        return data
        # Revert intersections



    def load_semaphores(self):
        semaphores = []
        for idx, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == 'Z':
                    semaphores.append(
                        SemaphoreSet(
                            self.grid, self.locks, idx, j, cycle_duration=10, grace_period=3
                        )
                    )
        return semaphores

    def __str__(self):
        return self.grid_to_str(self.grid)

    def parse_map(self, path):
        with open(path) as map_file:
            text = map_file.read()
            lines = text.split('\n')

        grid = [list(row) for row in lines]

        return grid

    def grid_to_str(self, grid):
        res = ''
        for row in grid:
            for col in row:
                if col in car_colors:
                    res += col
                else:
                    symbol_mapper = {
                        'U': '✅',
                        'B': '🔴',
                        'Z': '🌈'
                    }
                    res += symbol_mapper.get(col, col+' ')

            res += '\n'

        return res

    def locks_to_str(self):
        res = ''
        for idx, row in enumerate(self.locks):
            for j, col in enumerate(row):
                if col.locked():
                    res += 'B '
                else:
                    res += f'U '
            res += '\n'
        return res

    def pick_random_key(self, d: dict):
        return choice(
            list(
                d.keys()
            )
        )

    async def spawn_cars(self):
        cars_per_second = 3
        n_cars = 0
        while True:
            # Get state / spawn point
            state = self.pick_random_key(SPAWNS)
            next_state = self.pick_random_key(SPAWNS[state])
            x, y = SPAWNS[state][next_state]
            car = Car(
                    x,
                    y,
                    self.grid,
                    self.graph,
                    self.locks,
                    state, 
                    next_state,
                    self.intersections
                )
            self.cars[n_cars] = car
            n_cars += 1
            asyncio.create_task(car.drive())
            await asyncio.sleep(1 / cars_per_second)

    async def start_semaphores(self):
        tasks = []
        for semaphore in self.semaphores:
            tasks.append(
                asyncio.gather(
                    asyncio.create_task(semaphore.set_locks()),
                    asyncio.create_task(semaphore.run())
                )

            )
        await asyncio.gather(*tasks)

    async def run(self):
        # Main loop
        spawn_task = asyncio.create_task(self.spawn_cars())
        semaphores_task = asyncio.create_task(self.start_semaphores())
        while True:
            if spawn_task.done():
                print('I dont know why but every car exploded')
                break
            if semaphores_task.done():
                print('I dont know why but every semaphore exploded')
                break
            # Force loop to run at least every n seconds
            timer_task = asyncio.create_task(asyncio.sleep(0.5))
            await self.render_map()
            await timer_task

    def validate_coord(self, i, j):
        return \
            i >= 0 and\
            i < len(self.grid) and\
            j >= 0 and\
            j < len(self.grid[0])

    async def render_map(self):
        '''
          This might be non-efficient, pls fix razonixx
        '''
        # Make a tmp map for each time we render
        grid = [row[::] for row in self.grid]

        symbol_mapper = {
            '>': '-',
            '<': '-',
            'v': '|',
            '^': '|',
            'Y': 'X'

        }

        # Replace special symbols
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col in symbol_mapper:
                    grid[i][j] = symbol_mapper.get(col, '🤡')

        # Put each car in its x,y coords
        keys = list(self.cars.keys())
        for idx in keys:
            car = self.cars[idx]

            i, j = car.i, car.j

            # If Car is out grid kill it
            if not self.validate_coord(i, j) or not car.run:
                car.run = False
                if car.prev_lock.locked():
                    car.prev_lock.release()
                del self.cars[idx]
                continue

            grid[i][j] = car.color

        # Print values

        clear()
        #[print(self.cars[car].street) for car in self.cars]
        print(len(self.cars))
        #print(
        #    self.grid_to_str(grid)
        #)
        print(
            self.grid_to_str(grid)
        )
