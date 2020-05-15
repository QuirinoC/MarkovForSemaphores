from random import choice
import asyncio
from random import random, randint

car_colors = ['🚖', '🚗', '🚘', '🚙', '🚍']
dir_options = ['up', 'down', 'left', 'right']

class Car:
  def __init__(self,
               x,
               y,
               speed=1,
               color=None,
               dir=None,
              ):

    self.x     = x
    self.y     = y
    self.speed = randint(1,5) if speed is None else speed
    self.color = choice(car_colors) if color is None else car_colors[color]
    self.dir   = choice(dir_options) if dir is None else dir
    self.run   = True

  def __str__(self):
    return self.color

  def __repr__(self):
    return f'{self.color} ({self.x},{self.y})'

  def move(self):
    dir_map = {
      'up'   : (0 ,1),
      'down' : (0,-1),
      'left' : (-1,0),
      'right' : (1 ,0),
    }
    x, y = dir_map[self.dir]
    self.x += x
    self.y += y

  async def vroom(self):
    while self.run:
      self.move()
      await asyncio.sleep(1)

    