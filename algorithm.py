import numpy as np


class Algorithm:
    def __init__(self, _input, debug=False):
        self.input = _input
        self.debug = debug
        self.solution = None

    def find_solution(self):
        self.solution = (0,[])
        return self.solution

    def verify_solution(self):
        return True

    def score_solution(self):
        pass
