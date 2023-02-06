import numpy as np
from scipy.stats import logistic
import matplotlib.pyplot as plt
import math
import functions
import config

def test_config():

    X = np.linspace(-10, 10, 1000)
    #func = config.DISTANCE_SCORE_FARM
    func = config.ATTRACTION_FARM

    y = [func.eval(x) for x in X]

    plt.plot(X, y)
    #plt.yscale('log')
    plt.show()


def test_logistic():

    X = np.linspace(-10, 10, 1000)
    func = functions.sigmoid(offset=3, slope=3, scale=-1, intercept=1)

    y = [func.eval(x) for x in X]


    plt.plot(X, y)
    plt.show()



test_config()


