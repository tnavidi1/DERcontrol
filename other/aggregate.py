import numpy as np
import random

'''
Calculates the average of the maximum loads (maximum of one day) over all days
'''
def daily_average(l, time_resolution):
    #assuming that the time_resolution is smaller than 1440 (number of minutes per day)
    number_of_days = (time_resolution * np.size(l)) / 1440
    sum = 0
    split_array = np.array_split(l, number_of_days)
    for i in range(number_of_days):
        sum += np.max(split_array[i])
    return sum / number_of_days

'''
This function aggregates the load profiles of several nodes until the maximum has 
reached a specified value
'''
def aggregate(data, max_loads, daily_max = False, time_resolution = np.nan):
    if daily_max == False:
        new_data = np.zeros((np.size(max_loads), np.size(data, 1)), dtype=np.float64)
        for i in range(len(max_loads)):
            while np.max(new_data[i]) < max_loads[i]:
                num_row = np.random.randint(0, len(data) - 1)
                new_data[i] += data[num_row]
            adjustment_rate = np.max(new_data[i]) / max_loads[i]
            new_data[i] /= adjustment_rate
        return new_data

    else:
        if time_resolution == np. nan:
            return []
        else:
            new_data = np.zeros((np.size(max_loads), np.size(data, 1)), dtype=np.float64)
            for i in range(len(max_loads)):
                while daily_average(new_data[i], time_resolution) < max_loads[i]:
                    num_row = np.random.randint(0, len(data) - 1)
                    new_data[i] += data[num_row]
                adjustment_rate = np.max(new_data[i]) / max_loads[i]
                new_data[i] /= adjustment_rate
            return new_data

if __name__ == '__main__':
    #data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')
    data = np.array([[1, 4, 1, 2, 1], [1, 2, 1, 2, 3], [0, 4, 3, 3, 1]])
    max_loads = [19, 8]
    new_data = aggregate(data, max_loads)
    print("new_data: " + str(new_data))
    new_data = aggregate(data, max_loads, True, 900)
    print("new_data: " + str(new_data))