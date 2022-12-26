import numpy as np
from scipy.stats import logistic
import matplotlib.pyplot as plt
import math
import functions
def test_logistic():

    X = np.linspace(-10, 10, 1000)
    func = functions.sigmoid(offset=3, slope=3, scale=-1, intercept=1)

    y = [func.eval(x) for x in X]


    plt.plot(X, y)
    plt.show()



test_logistic()


