
# coding: utf-8

# In[48]:

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
import testStationarity
from sklearn.metrics import mean_absolute_error
import math
# np.seterr(all='warn')
# #np.seterr(all='raise')

# import warnings
# warnings.filterwarnings("error")


# # PreProcessing Data

# In[43]:

data = pd.read_csv('prices.csv')
print data.head(10)
print '\n Data Types:'
print data.dtypes


# In[44]:

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('prices2.csv', parse_dates=True, index_col='Time',date_parser=dateparse)
print data.head()


# ## Make the data Stationary

# In[53]:

ts = data['Price']
ts_log = np.log(ts)

'''We compute diff to make the data closer to linearity'''
ts_log_diff = ts_log - ts_log.shift()

'''Remove null values in place'''
ts_log_diff.dropna(inplace=True)


# In[46]:

'''ACF is applied to compute MA value; '''
lag_acf = acf(ts_log_diff, nlags=40)
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')
plt.show()

lag_pacf = pacf(ts_log_diff, nlags=40, method='ols')
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()


# In[97]:


def predictPrice(p, q):
    mae, predictions_ARIMA = None, None
    try:
        model = ARIMA(ts_log, order=(p,1,q))  
        results_ARIMA = model.fit(disp=-1)
        predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
        predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
        predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
        for ind, val in predictions_ARIMA_diff_cumsum.iteritems():
            predictions_ARIMA_log[ind] =  predictions_ARIMA_log[ind] + val
        predictions_ARIMA = np.exp(predictions_ARIMA_log)
        #rmse = np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts))
        mae = mean_absolute_error(ts, predictions_ARIMA)

    except:
        pass
    return mae, predictions_ARIMA

minMae = 9999
for i in xrange(1,6):
    for j in xrange(1,5):
        mae, predictions_ARIMA = predictPrice(i,j)
        
        if mae and not predictions_ARIMA.empty and mae < minMae:
            minMae = mae
            p, q = i, j
            best_predictions_ARIMA = predictions_ARIMA

print best_predictions_ARIMA.head(10)
print p, q
plt.plot(ts, color='blue')
plt.plot(best_predictions_ARIMA, color='green')
#plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
plt.title('RMSE: %.4f'% mean_absolute_error(ts, best_predictions_ARIMA))
plt.show()


# In[96]:




# In[ ]:



