import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sampling import Resampling
from pyramid.arima import auto_arima


data_raw = np.genfromtxt('agg_load_123_july.csv', delimiter=',')
data_raw = data_raw[:, 1:]
data_res = Resampling(data_raw.T, 1, 60)
data = data_res.downsampling(data_raw.T, 1, 60)
data = data.T
train_data = data[:576, :]
test_data = data[576:, :]

#model_fit = auto_arima(data[:, 25], start_p=1, start_q=1, start_P=1, start_Q=1,
#                  max_p=10, max_q=10, max_P=10, max_Q=10, m=24, seasonal=True,
#                  stepwise=True, suppress_warnings=False,
#                  error_action='ignore')
#model_fit.summary()

my_order = (3, 0, 3)
my_seasonal_order = (3, 0, 3, 24)
model = SARIMAX(data[:, 11], order=my_order, seasonal_order=my_seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit(maxiter=50)
yhat = model_fit.forecast(24)

#reshaped_data = np.reshape(data[:, 11], (24, 31))
#data_mean = np.reshape(np.mean(reshaped_data, 1), (24, 1))

data_mean = np.reshape((data[:24, 11]), (24, 1))
reshaped_yhat = np.reshape(yhat, (24, 1))

diff = np.abs((data_mean - reshaped_yhat) / data_mean) * 100
print("diff", diff)


if __name__ == '__main__':
    print('program ended')
