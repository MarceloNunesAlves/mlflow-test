import random

def calcRandom(_amplitude, _perc_random=5):
    return random.uniform(0-((_perc_random*_amplitude)/100),((_perc_random*_amplitude)/100))