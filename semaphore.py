import asyncio
from random import shuffle
class SemaphoreSet:
    def __init__(self, grid: [[str]], locks: [[asyncio.Lock()]], i: int, j: int, cycle_duration: int = 10, grace_period=5, speed_multiplier=1.0,RIGHT_TURN=True, STATE=0):
        top = [
            (i + 0, j + 3),
            (i + 0, j + 2),
            (i + 0, j + 1),
        ]
        bottom = [
            (i + 7, j + 4),
            (i + 7, j + 5),
            (i + 7, j + 6),
        ]
        left = [
            (i + 4, j + 0),
            (i + 5, j + 0),
            (i + 6, j + 0),
        ]
        right = [
            (i + 3, j + 7),
            (i + 2, j + 7),
            (i + 1, j + 7),
        ]

        self.i = i
        self.j = j
        self.grid = grid
        self.locks = locks
        self.cycle_duration = cycle_duration
        self.grace_period = grace_period
        self.semaphores = {
            'top'   : top,
            'bottom': bottom,
            'left'  : left,
            'right' : right,
        }
        self.SPEED_MULTIPLIER = speed_multiplier
        self.STATE = STATE

        self.metadata = {
            'right_turn' : RIGHT_TURN,
        }


    
    def __str__(self):
        return str((self.i,self.j))

    def __repr__(self):
        return self.__str__()

    async def set_locks(self):


        for name, locks in self.semaphores.items():
            if self.metadata['right_turn']: locks = locks[:-1]
            for i,j in locks[:]:
                self.grid[i][j] = 'B'
                await self.locks[i][j].acquire()

    def print_locks(self):
        res = ''
        for idx, row in enumerate(self.locks):
            for j, col in enumerate(row):
                res += '❇️' if col.locked() else 'X'
                res += ' '
            res += '\n'

    async def acquire_semaphore(self, semaphore):
        i, j = semaphore
        # Release the semaphores on unblocked
        self.locks[i][j].release()
        self.grid[i][j] = 'U'

        # Await required time
        await asyncio.sleep(self.cycle_duration * self.SPEED_MULTIPLIER)

        # Block semaphores again
        await self.locks[i][j].acquire()
        self.grid[i][j] = 'B'

    async def acquire_semaphores(self, semaphores):
        tasks = []
        for semaphore in semaphores:
            tasks.append(self.acquire_semaphore(semaphore))

        await asyncio.gather(*tasks)

    async def run(self):
        '''
        Cycle is defined this way: 
            - First the inner turns are made for each axis
            - Then going straight and turning right
        '''
        R = 0 if self.metadata['right_turn'] else 1
        STATES = {
            0 : {
                'side_order' :  [('top', 'bottom'), ('left', 'right')],
                'lights_order' : [(0,1), (1,2 + R)]
            },
            1 : {
                'side_order' : [['top'],['bottom'],['left'],['right'],],
                'lights_order' : [(0,2), (2, 2 + R)]
            }
        }

        STATE = STATES[self.STATE]

        side_order = STATE['side_order']
        lights_order = STATE['lights_order']

        shuffle(side_order)
        shuffle(lights_order)

        while True:
            for k in side_order:
                for x,y in lights_order:
                    tasks = []
                    for k_ in k:
                        tasks.append(
                            asyncio.create_task(
                            self.acquire_semaphores(self.semaphores[k_][x:y])
                            )
                        )
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(self.grace_period * self.SPEED_MULTIPLIER)

    async def render_locks(self):
        while True:
            clear()
            self.print_locks()
            await asyncio.sleep(0.5)

# This is only for test purposes
async def main():
    locks = [[asyncio.Lock() for j in range(100)] for i in range(50)]
    zapopan_map = Map('mapa_symbols.txt', {})
    for i in range(0, 10 * 8, 8):
        sem = SemaphoreSet(locks, i,i)
        asyncio.create_task(sem.run())
    render_task = asyncio.create_task(sem.render_locks())

    await render_task


if __name__=='__main__':
    import os
    clear = lambda: os.system('clear')
    asyncio.run(main())