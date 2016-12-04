import pandas as pd
import numpy as np
import matplotlib.pylab as plt
#%matplotlib inline
from matplotlib.pylab import rcParams
import datetime
from dateutil.relativedelta import relativedelta
#import seaborn as sns
import statsmodels.api as sm  
from statsmodels.tsa.stattools import acf  
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose
rcParams['figure.figsize'] = 15, 6

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('dat/Automotive/B00FDQPCR2.csv', parse_dates=['Time'],date_parser=dateparse)
print data.head()
#data = pd.read_csv('dat/Automotive/B00FDQPCR2.csv')
#print data.head()
print '\n Data Types:'
print data.dtypes

print data.index

ts_x = data['Time']
ts_y = data['Price']
print type(data)


#plt.plot(ts_x,ts_y)
#plt.show()
data.reset_index(inplace=True)
data['Time'] = pd.to_datetime(data['Time'])
data = data.set_index('Time')
decomposition = seasonal_decompose(data.Price,freq = 12)  
fig = plt.figure()  
fig = decomposition.plot()  
fig.set_size_inches(15, 8)
plt.show()
