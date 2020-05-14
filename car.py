from random import choice
import asyncio
from random import random

car_colors = {0: '🚖', 1: '🚗', 2: '🚘', 3: '🚙', 4: '🚍'}

class Car:
  def __init__(self,
               speed=1,
               color=None,
               dir=None,
               x=None,
               y=None):

    self.speed = speed
    self.color = choice(car_colors) if color is None else car_colors[color]
    self.x = x
    self.y = y
    self.dir   = dir

  def __str__(self):
    return self.color

  def __repr__(self):
    return self.color

  def move(self):
    dir_map = {
      'up'   : (0 ,1),
      'down' : (0,-1),
      'left' : (-1,0),
      'down' : (1 ,0),
    }
    x, y = dir_map[self.dir]
    self.x += x
    self.y += y

  async def vroom(self, map):
    while True:
      await asyncio.sleep(random() * 10)
      print(f'{self}, VROOOOM!')