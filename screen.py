import curses
from curses.textpad import Textbox, rectangle
from time import sleep
import asyncio

class Screen:
    def __init__(self):
        self.stdscr = curses.initscr()

    async def render(self, data):
        self.stdscr.clear()
        for idx, row in enumerate(data.split('\n')):
            self.stdscr.addstr(idx,0, str(row))
        self.stdscr.refresh()

async def main():
    s = Screen([1,2,3,4])
    await s.render()

if __name__=='__main__': asyncio.run(main())