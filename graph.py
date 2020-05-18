from random import random

class Graph:
    def __init__(self, path='graph.txt'):
        self.graph = self.parse_graph(path)

    def parse_graph(self, path):
        with open(path, 'r') as f:
            data = eval(f.read())
        return data

    def parse_table(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        graph_data = [[float(val) for val in row.split(',')] for row in lines]

        for idx, row in enumerate(graph_data):
            assert round(
                sum(row), 4) == 1, f'Non markovian graph detected | {idx} | {row} | {sum(row)}'

        return graph_data

    def decide(self, current_state):
        node = self.graph[current_state]
        accum = 0
        limit = random()
        for state, p in node.items():
            accum += p
            if limit < accum:
                return state
