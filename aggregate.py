"""
Do not use future division use numpy arrays
data = np.array(data,dtype=float)
"""
from __future__ import division

import numpy as np
import random

def daily_average(l, time_resolution):
    """
    we dont want to compare the daily average we want to compare the average daily maximum
    To do this we would find the maximum value for each day
    Then average together every day's maximum value

    """
    s = sum(l)
    time_total = time_resolution * len(l)
    daily_average = 1440 * (s / time_total)
    return daily_average

def aggregate(data, max_loads, daily_max = False, time_resolution = np.nan):
    """
    It is good practice to use the triple quotes and a few sentences about what the object or function does.
    Inputs: data - description
            etc

    Outputs: new_data - description
    """
    if daily_max == False:
        new_data = []
        adjustment_rate = 0
        for i in range(len(max_loads)):
            """ If you want to initialize an array use np.zeros(size)
            """
            temp = [0] * len(data[0])
            """
            not good practice to use while True and if break
            Just put not if statement in the while loop
            """
            while True:
                num_row = random.randint(0, len(data) - 1)
                for j in range(len(temp)):
                    temp[j] +=data[num_row][j]
                if max(temp) > max_loads[i]:
                    adjustment_rate = max(temp) / max_loads[i]
                    break
            temp[:] = [x // adjustment_rate for x in temp]
            new_data.append(temp)
        return new_data
    else:
        if time_resolution == np.nan:
            return []
        else:
            new_data = []
            adjustment_rate = 0
            for i in range(len(max_loads)):
                temp = [0] * len(data[0])
                """
                not good practice to use while True and if break
                Just put not if statement in the while loop
                """
                while True:
                    num_row = random.randint(0, len(data) - 1)
                    for j in range(len(temp)):
                        temp[j] += data[num_row][j]
                    if daily_average(temp, time_resolution) > max_loads[i]:
                        adjustment_rate = daily_average(temp, time_resolution) / max_loads[i]
                        break
                temp[:] = [x // adjustment_rate for x in temp]
                new_data.append(temp)
                """
                instead of using append, initialize the array to the size wanted using np.zeros(size) first
                This is much faster
                then add elements using numpy indexing new_data[i,:] = time series
                """
            return new_data

if __name__ == '__main__':
    #data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')
    data = [[1, 4, 1, 2, 1], [1, 2, 1, 2, 3], [0, 4, 3, 3, 1]]
    max_loads = [15, 8]
    new_data = aggregate(data, max_loads)
    print("new_data: " + str(new_data))
    new_data = aggregate(data, max_loads, True, 900)
    print("new_data: " + str(new_data))