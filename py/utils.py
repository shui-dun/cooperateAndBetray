import random
from person import *


def posIntGauss(mu, gamma):
    n = random.gauss(mu, gamma)
    if n < 0:
        n = 0
    n = int(n)
    return n


def rouletteWheelSelection(fitness):
    sumFits = sum(fitness)
    rndPoint = random.uniform(0, sumFits)
    accumulator = 0.0
    for ind, val in enumerate(fitness):
        accumulator += val
        if accumulator >= rndPoint:
            return ind
