import numpy as np
import math
class exp:

    def __init__(self, scale, mean, offset):

        self._scale = scale
        self._mean = mean
        self._offset = offset

    def eval(self, inp):

        return self._scale*np.exp(self._mean*inp) + self._offset

class sigmoid:
    "Numerically-stable sigmoid function."

    def __init__(self, scale=1, slope=1, offset=0, intercept=0):

        self._scale = scale
        self._slope = slope
        self._offset = offset
        self._intercept = intercept


    def eval(self, inp):
        if inp >= 0:
            z = math.exp(-1*self._slope*(self._offset-inp))
            return (self._scale / (1 + z)) + self._intercept
        else:
            z = math.exp(self._slope*(self._offset-inp))
            return ((self._scale*z) / (1 + z)) + self._intercept


class lookup:

    def __init__(self, values=None, default=None):

        self._lookup = values
        if self._lookup is None:
            self._lookup = {}
        self._default = default

    def add_value(self, key, value):
        self._lookup[key] = value

    def set_default(self, default):
        self._default = default

    def eval(self, inp):
        return self._lookup.get(inp, self._default)
