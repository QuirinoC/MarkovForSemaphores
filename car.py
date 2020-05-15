from random import choice
import asyncio
from random import random, randint

car_colors = ['🚖', '🚗', '🚘', '🚙', '🚍']
dir_options = ['up', 'down', 'left', 'right']
street_options = [0, 1, 2, 3] # A, B, C, D

class Car:
  def __init__(self,
               x,
               y,
               graph,
               speed=1,
               color=None,
               dir=None,
               street=None,
              ):

    self.x      = x
    self.y      = y
    self.graph  = graph
    self.speed  = randint(1,5) if speed is None else speed
    self.color  = choice(car_colors) if color is None else car_colors[color]
    self.dir    = choice(dir_options) if dir is None else dir
    self.street = choice(street_options) if street is None else street
    self.run    = True
    self.f = open("log.txt", "w")

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
    self.decide()
    x, y = dir_map[self.dir]
    self.x += x
    self.y += y

  def decide(self):
    self.f.writelines("Street: " + self.street + "\n")
    graphRow = self.graph[self.street]
    accum = 0
    limit = random()
    for i, p in enumerate(graphRow):
      accum += p
      if limit < accum:
        self.dir = dir_options[i]

  async def vroom(self):
    while self.run:
      self.move()
      await asyncio.sleep(1)

    