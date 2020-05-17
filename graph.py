from random import random

metadata = {
    'spawns' : [
        # Spawns from the left side
        (13,0 ),
        (14,0 ),
        (15,0 ),
        (29,0 ),
        (30,0 ),
        (31,0 ),
        # Spawns from top
        (0 ,21),
        (0 ,22),
        (0 ,23),
        (0 ,59),
        (0 ,60),
        (0 ,61),
        # Spawns from right
        (10,85),
        (11,85),
        (12,85),
        (26,85),
        (27,85),
        (28,85),
        # Spawns from bottom
        (41,24),
        (41,25),
        (41,26),
        (41,62),
        (41,63),
        (41,64)
    ]
}

class Graph:
    def __init__(self, path='graph.txt'):
        self.graph = self.parse_graph(path)
        self.metadata = metadata
    def parse_graph(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        graph_data = [[float(val) for val in row.split(',')] for row in lines]

        for idx, row in enumerate(graph_data):
            assert round(
                sum(row), 4) == 1, f'Non markovian graph detected | {idx} | {row} | {sum(row)}'

        return graph_data

    def decide(self, current_state):
        row = self.graph[current_state]
        accum = 0
        limit = random()
        for idx, p in enumerate(row):
            accum += p
            if limit < accum:
                return idx
                break


'''
        # A    B    C    D    E    F    G    H    I    J    K    L
       [[.25, .25, .25, 0.0, 0.0, .25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # A
        [.25, .25, .25, 0.0, 0.0, .25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # B
        [.10, .10, .10, .10, .10, .25, .25, 0.0, 0.0, 0.0, 0.0, 0.0], # C
        [0.0, 0.0, .25, .25, .25, 0.0, .25, 0.0, 0.0, 0.0, 0.0, 0.0], # D
        [0.0, 0.0, .25, .25, .25, 0.0, .25, 0.0, 0.0, 0.0, 0.0, 0.0], # E
        [.10, .10, .25, 0.0, 0.0, .10, 0.0, .10, .10, .25, 0.0, 0.0], # F
        [0.0, 0.0, .25, .10, .10, 0.0, .10, 0.0, 0.0, .25, .10, .10], # G
        [0.0, 0.0, 0.0, 0.0, 0.0, .25, 0.0, .25, .25, .25, 0.0, 0.0], # H
        [0.0, 0.0, 0.0, 0.0, 0.0, .25, 0.0, .25, .25, .25, 0.0, 0.0], # I
        [0.0, 0.0, 0.0, 0.0, 0.0, .25, .25, .10, .10, .10, .10, .10], # J
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .25, 0.0, 0.0, .25, .25, .25], # K
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .25, 0.0, 0.0, .25, .25, .25]] # L
'''
