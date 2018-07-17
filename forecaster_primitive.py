"""
Forecaster object, with predict method, intaking 2-d array of data NODESxTIME, returning another array of the same size but with predicted data using random gaussian error with stddv provided to the object class.
No for loops.
"""

import numpy as np


class Forecaster:
    def __init__(self, error):
        self.error = error

    def predict(self, data):
        mu, sigma = 0, self.error
        data_size = data.shape
        result = data * (1 + np.random.normal(mu, sigma, data_size))
        return result


if __name__ == '__main__':
    fore_1 = Forecaster(error=0.1)
    data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')  # type: object
    pred_1 = fore_1.predict(data)
    print pred_1
    print data
