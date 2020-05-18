import asyncio
class SemaphoreSet:
    def __init__(self, grid: [[str]], locks: [[asyncio.Lock()]], i: int, j: int, cycle_duration: int = 3):
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
        self.semaphores = {
            'top'   : top,
            'bottom': bottom,
            'left'  : left,
            'right' : right,
        }
    
    def __str__(self):
        return str((self.i,self.j))

    def __repr__(self):
        return self.__str__()

    async def set_locks(self):
        for name, locks in self.semaphores.items():
            for i,j in locks:
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
        await asyncio.sleep(self.cycle_duration)

        # Block semaphores again
        await self.locks[i][j].acquire()
        self.grid[i][j] = 'B'


    async def run(self):
        '''
        Cycle is defined this way: 
            - First the inner turns are made for each axis
            - Then going straight and turning right
        '''

        # Right turn is always on
        for key, indices in self.semaphores.items():
            i, j = indices[-1]
            self.locks[i][j].release()
            self.grid[i][j] = 'U'

        while True:
            # Left turns for vertical 
            turn_left_top = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['top'][0])
            )
            turn_left_bottom = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['bottom'][0])
            )
            await asyncio.gather(turn_left_top, turn_left_bottom)

            # Left turns for horizontal
            turn_left_left = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['left'][0])
            )
            turn_left_right = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['right'][0])
            )
            await asyncio.gather(turn_left_left, turn_left_right)

            # Vertical and right turns
            horizontal_top = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['top'][1])
            )
            horizontal_bottom = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['bottom'][1])
            )
            await asyncio.gather(horizontal_top, horizontal_bottom)

            # Horizontal and right turns
            horizontal_left = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['left'][1])
            )
            horizontal_right = asyncio.create_task(
                self.acquire_semaphore(self.semaphores['right'][1])
            )
            await asyncio.gather(horizontal_left, horizontal_top)

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