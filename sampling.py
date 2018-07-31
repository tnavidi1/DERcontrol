"""
NOTE : has a lot of for loops.

Assuming that tmin is multiple of t or vice versa
"""

import numpy as np

class Resampling:
	"""
	It is good practice to use the triple quotes and a few sentences about what the object or function does.
	Inputs: data - description
			t - description
			tnew - description

	Outputs: downsampled - description
	"""

	def __init__(self, data, t, tnew):
		self.data = data
		self.t = t
		self.tnew = tnew
	def downsampling(self, data, t, tnew):
		"""
		use numpy array instead of python list
		downsampled = np.zeros(size of new array)
		"""
		downsampled = []
		t_ratio = tnew // t
		node_num = 0
		"""
		try using numpy array indexing
		look up numpy array indexing on google to learn about it
		It might be possible to do this in one line
		downsampled = data[:,0:-1:t_ratio] This may not be correct. It is your job to check this.
		Main Concept: numpy indexing has [] after variable with first : representing all the rows then
					after the , is the columns. For more than 2 dimensionnal array each , separates the next dimension.
					In the columns, the 0 means first element : separates and -1 is the last element. : separates and the
					the final number is the number of spaces between the first and last that are sampled
					It is possible to simplify 0:-1:t to ::t because the entire column is implied by just typing : as is done for rows
		Check all of this with a google search for numpy indexing
		"""  

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
		"""
		use numpy array instead of python list
		upsampled = np.zeros(size of new array)
		"""
		upsampled = []
		upsampled_final = []
		node_num = 0
		"""
		you can use . to make things into a float
		highly recommended for division
		min_per_day = 1440.
		to make whole numpy arrays into floats
		data = np.array(data,dtype=float)
		It is good practice to put things like this into the begining of your function to make them into the proper data type
		This way you dont have to assume the user input the correct data type for your function to work
		"""

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
		"""
		Sigma should be calculated from the data not hardcoded.
		google search numpy standard deviation to get the value
		It will require all of the data, so do not sum it up like you do above
		Just organize it into an array of shape 24 X number of days and use numpy mean and standard deviation on it
		use np.zeros((24,days)) to initialize the shape first
		"""
		sigma = 0.1
		for node in upsampled:
			for time in node:
				for i in range(t_ratio):
					upsampled_final[node_num].append([np.random.normal(time, sigma)])
			node_num += 1
		return upsampled_final

if __name__ == '__main__':
	t = 5
	tnew = 1
	data = np.genfromtxt('res_avg_load_data_5min_2days_no_headers.csv', delimiter=',')
	sample = Resampling(data, t, tnew)
	"""
	combine the 2 functions into one function and put this if statement in the beginning
	"""
	if t > tnew:
		ret = sample.upsampling(data, t, tnew)
	else:
		ret = sample.downsampling(data, t, tnew)
	print ret
	print data