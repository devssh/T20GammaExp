import numpy as np
from umpire import not_out, is_out
from run_rate_distribution import gamma_distribution


class Player:
    def __init__(self, name, run_rate, chance_to_get_out=0.1):
        if run_rate < 6 or run_rate > 36:
            raise ValueError("Invalid run rate per over")
        if chance_to_get_out < 0 or chance_to_get_out > 1:
            raise ValueError("Chance to get out is between 0 and 1")
        self.name = name
        self.chance_to_get_out = chance_to_get_out
        self.run_rate = run_rate
        self.pdf = gamma_distribution(run_rate)

    def out_status(self):
        return np.random.choice([is_out, not_out], p=[self.chance_to_get_out, 1 - self.chance_to_get_out])

    def bat(self, show_pdf=False):
        if show_pdf:
            print(self.pdf)
        return self.out_status(), np.random.choice([1, 2, 3, 4, 5, 6], p=self.pdf)

    def __str__(self):
        return "Player(" + self.name + ", " + str(self.run_rate) + ", " + str(self.chance_to_get_out) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name
