overs_left = 4
runs_to_win = 40
wickets_left = 3
number_of_balls_in_over = 6

import numpy as np
from scipy.stats import gamma
import math


class Player:
    def __init__(self, name, run_rate, chance_to_get_out=2):
        if run_rate < 6 or run_rate > 36:
            raise ValueError("Invalid run rate per over")
        self.name = name
        self.chance_to_get_out = chance_to_get_out
        self.run_rate = run_rate

        def gamma_distribution(run_rate_given):
            run_rate_per_ball = run_rate_given / number_of_balls_in_over
            param = 2.5
            # scale_dict = {1: 1, 2: 1, 3: 1, 4: 1.08, 5: 1.11, 6: 1.8, 7: 1.8 * 5}
            # scale_dict = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 10}
            # scale = scale_dict[int(param) + 1]
            scale = 1
            loc_factor = run_rate_per_ball - param
            Lambda = 1
            exponential_distribution_correction = Lambda * math.exp(Lambda * run_rate_per_ball)
            loc = loc_factor + exponential_distribution_correction  # -2 -0.09 0.1 0.27  0.3 1
            pdf = gamma.pdf([2, 3, 4, 5], a=param, loc=loc, scale=scale)
            cdf = gamma.pdf([*list(range(-12, 2)), *list(range(6, 24))], a=param, loc=loc, scale=scale)
            cdf = [sum(cdf[0: 14]), sum(cdf[14:])]
            pdf = np.array([cdf[0], *pdf, cdf[1]])
            pdf = pdf / sum(pdf)
            return pdf

        self.pdf = gamma_distribution(run_rate)

    def bat(self, show_pdf=False):
        if show_pdf:
            print(self.pdf)
        return np.random.choice([1, 2, 3, 4, 5, 6], p=self.pdf)


def test(run_rate):
    kirat = Player('Kirat Boli', run_rate, 4)
    x = [kirat.bat() for i in range(1, 1000)]
    return sum(x) / 1000


if __name__ == '__main__':
    kirat = Player('Kirat Boli', 30, 4)
    Player('NS Nodhi', 10)
    Player('R Rumrah', 9)
    Player('Shashi Henra', 6)
    print("test")
    # Player('x', 37)
    print([(i, test(i)) for i in range(6, 37)])
