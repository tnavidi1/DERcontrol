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
		downsampled = []
		t_ratio = tnew // t
		node_num = 0
		for node in data:
			i = 0
			time_sum = 0
			for time in node:
				if i >= t_ratio:
					avg = time_sum / t_ratio
					downsampled[node_num].append([avg])
					avg = 0
					i = 0
				else:
					i += 1
					time_sum += time
			node_num += 1
		return downsampled

	def upsampling(self, data, t, tnew):
		upsampled = []
		upsampled_final = []
		node_num = 0
		min_per_day = 1440
		t_ratio = t // tnew
		pts_per_day = min_per_day // t
		total_pts = len(data[0])
		days = total_pts // pts_per_day
		for node in data:
			for i in range(pts_per_day):
				tot_at_time_of_day = 0
				for j in range(days):
					tot_at_time_of_day += node[i + j]
				upsampled[node_num].append([tot_at_time_of_day / days])
			node_num += 1
		node_num = 0
		sigma = 0.1
		for node in upsampled:
			for time in node:
				for i in range(t_ratio):
					upsampled_final[node_num].append([np.random.normal(time, sigma)])
			node_num += 1
		return upsampled_final

if __name__ == '__main__':
	t = 5
	tnew = 10
	data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')
	sample = Resampling(data, t, tnew)
	if t > tnew:
		ret = sample.upsampling(data, t, tnew)
	else:
		ret = sample.downsampling(data, t, tnew)
	print ret
	print data