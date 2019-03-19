import numpy as np
from umpire import out


class Player:
    def __init__(self, name, pdf):
        if abs(sum(pdf) - 1) > 0.01:
            raise ValueError("Probability Density Function should sum to 1")
        self.name = name
        self.pdf = pdf

    def bat(self):
        outcomes = [0, 1, 2, 3, 4, 5, 6, out]
        return np.random.choice(outcomes, p=self.pdf)

    def __str__(self):
        return "Player(" + self.name + ", [" + ",".join([str(outcome) for outcome in self.pdf]) + "])"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name
