import numpy as np

HEADS = "Heads"
TAILS = "Tails"


def flip_coin():
    return select_outcome([HEADS, TAILS], [0.5, 0.5])


def select_outcome(choices, pdf):
    return np.random.choice(choices, p=pdf)
