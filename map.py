class Map():
  def __init__(self, path):
    self.grid = self.parse_map(path)

  def parse_map(self,path):
    with open(path) as map_file:
      text = map_file.read()
      lines = text.split('\n')
    grid = [list(row) for row in lines]
    return grid

  def __str__(self):
    return '\n'.join([' '.join(row) for row in self.grid])
    

if __name__ == "__main__":
  m = Map('mapa_4.txt')
  print(m)