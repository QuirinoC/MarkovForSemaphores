from os import system, name
import asyncio
from car import Car, car_colors
from random import choice
from semaphore import SemaphoreSet

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

cls_cmd = 'clear' if name == 'posix' else 'cls'

street_light_dict = {
    (10,21):{'x':10, 'y':21, 'green_length':5, 'red_length':5, 'color':'red'},
    (10,22):{'x':10, 'y':22, 'green_length':5, 'red_length':5, 'color':'red'},
    (10,23):{'x':10, 'y':23, 'green_length':5, 'red_length':5, 'color':'red'},
}

def clear():
    system(cls_cmd)

class Map():
    def __init__(self, path: str, graph: [[str]], cars: dict = {}):
        self.grid = self.parse_map(path)
        self.graph = graph
        # Keep track of the cars
        self.cars = cars
        self.locks = [[asyncio.Lock() for j in range(len(self.grid[0]))] for i in range(len(self.grid))]
        self.semaphores = self.load_semaphores()
    
    def load_semaphores(self):
        semaphores = []
        for idx, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == 'S':
                    semaphores.append(
                        SemaphoreSet(
                            self.grid, self.locks, idx, j, cycle_duration=3
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
                    res += f'{col} '
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

    async def spawn_cars(self):

        n_cars = 0
        while True:
            # Get next spawn point 
            x,y = choice(self.graph.metadata['spawns'])
            car = Car(x, y, self.grid, self.graph, self.locks, self.locks)
            self.cars[n_cars] = car; n_cars+=1
            asyncio.create_task(car.drive())
            await asyncio.sleep(0.1)

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
            timer_task = asyncio.create_task(asyncio.sleep(1))
            await self.render_map()
            await timer_task

    def validate_coord(self, i, j):
        return \
                i >= 0 and\
                i <  len(self.grid) and\
                j >=0 and\
                j <  len(self.grid[0])
        

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
            'S': '🇲🇲',
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
            if not self.validate_coord(i,j):
                car.run = False
                del self.cars[idx]
                continue
            
            grid[i][j] = car.color

        # Print values
        clear()
        print(len(self.cars))
        print(
            self.grid_to_str(grid)
        )
