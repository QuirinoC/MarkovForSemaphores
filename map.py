from os import system, name
import asyncio
from car import Car, car_colors

cls_cmd = 'clear' if name == 'posix' else 'cls'
def clear():
  system(cls_cmd)

class Map():
  def __init__(self, path: str, cars: dict = {}):
    self.grid = self.parse_map(path)
    # Keep track of the cars
    self.cars = cars

  def parse_map(self,path):
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
          res+=col
        else:
          res+=f'{col} '
      res+='\n'
    
    return res

  def __str__(self):
    return self.grid_to_str(self.grid)

  async def render_map(self):
    '''
      This might be non-efficient, pls fix razonixx
    '''
    while True:
      # Make a tmp map for each time we render
      grid = [row[::] for row in self.grid]

      # Put each car in its x,y coords
      for idx, car in self.cars.items():
        x,y = car.x, car.y
        grid[x][y] = car.color
        print(x,y, car.color)

      clear()
      print(
        self.grid_to_str(grid)
      )
      await asyncio.sleep(0.5)
      