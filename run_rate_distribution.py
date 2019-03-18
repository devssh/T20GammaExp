from game import number_of_balls_in_over
from scipy.stats import gamma
import math
import numpy as np


def gamma_distribution(run_rate_given):
    def exponential_error_correction_function(_run_rate):
        return (-1.1446 * 0.006688 * math.exp(1.1446 * (number_of_balls_in_over - _run_rate))) + 0.3411

    run_rate_per_ball = run_rate_given / number_of_balls_in_over
    param = 2.5
    run_rate = run_rate_per_ball + 1
    tail_correction = 0 if int(run_rate) < 6 else 0.1 if round(run_rate, 1) == 6 else 0.3 if int(run_rate) == 6 else 2
    scale = 1
    loc_factor = run_rate_per_ball - param
    loc = loc_factor + exponential_error_correction_function(run_rate_per_ball) + tail_correction
    pdf = gamma.pdf([2, 3, 4, 5], a=param, loc=loc, scale=scale)
    cdf = gamma.pdf([*list(range(-12, 2)), *list(range(6, 24))], a=param, loc=loc, scale=scale)
    cdf = [sum(cdf[0: 14]), sum(cdf[14:])]
    pdf = np.array([cdf[0], *pdf, cdf[1]])
    pdf = pdf / sum(pdf)
    return pdf
