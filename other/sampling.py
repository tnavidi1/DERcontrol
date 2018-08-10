"""
NOTE : has a lot of for loops.

Assuming that tmin is multiple of t or vice versa
"""

import numpy as np


class Resampling:
    def __init__(self, data, t, tnew):
        self.data = data
        self.t = t
        self.tnew = tnew

    def downsampling(self, data, t, tnew):
        t_ratio = tnew // t
        downsampled = np.zeros((np.size(data, 0), np.size(data, 1) / t_ratio))
        for i in range(np.size(downsampled, 0)):
            for j in range(np.size(downsampled, 1)):
                downsampled[i][j] = np.average(data[i][j:j+t_ratio+1])
        return downsampled


    def upsampling(self, data, t, tnew):
        std_dv = np.std(data)
        print(std_dv)
        t_ratio = t // tnew
        upsampled = np.zeros((np.size(data, 0), np.size(data, 1) * t_ratio))
        for i in range(np.size(upsampled, 0)):
            for j in range(np.size(upsampled, 1)):
                upsampled[i][j] = np.random.normal(data[i][j/t_ratio], std_dv)
        return upsampled



if __name__ == '__main__':
    t = 5
    tnew = 10
    data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')
    data = data[:,:5]
    sample = Resampling(data, t, tnew)
    if t > tnew:
        ret = sample.upsampling(data, t, tnew)
    else:
        ret = sample.downsampling(data, t, tnew)
    print np.size(ret, 1)
    print np.size(data, 1)
    print ret
    print data
