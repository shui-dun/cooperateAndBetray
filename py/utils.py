import random
from typing import List


# 高斯分布，但是返回非负整数
def posIntGauss(mu: float, gamma: float) -> int:
    n = random.gauss(mu, gamma)
    if n < 0:
        n = 0
    n = int(n)
    return n


# 轮盘赌选择法
def rouletteWheelSelection(fitness: List[float]) -> int:
    sumFits = sum(fitness)
    rndPoint = random.uniform(0, sumFits)
    accumulator = 0.0
    for ind, val in enumerate(fitness):
        accumulator += val
        if accumulator >= rndPoint:
            return ind
