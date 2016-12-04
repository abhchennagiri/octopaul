import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_absolute_error
import math

class ARIMAModel():

    def __init__(self):
        pass

    ############################# Data pre-processing functions. #################

    def readFile(self, fileName):
        '''This function reads the csv file which has first column as dates and 
         second column as prices into a DataFrame object and returns it.'''

        dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
        data = pd.read_csv(fileName, parse_dates=True, index_col='Time',date_parser=dateparse)
        return data
    

    def stationarizeData(data):
        
        ts = data['Price']
        ts_log = np.log(ts)
        '''We compute diff to make the data closer to leaniarity.'''
        ts_log_diff = ts_log - ts_log.shift()
        '''Remove null values in place'''
        ts_log_diff.dropna(inplace=True)    

        return ts,ts_log,ts_log_diff

    def test_stationarity(timeseries):

        #Determing rolling statistics
        rolmean = pd.rolling_mean(timeseries, window=12)
        rolstd = pd.rolling_std(timeseries, window=12)

        #Plot rolling statistics:
        orig = plt.plot(timeseries, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        #std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show()

        #Perform Dickey-Fuller test:
        print 'Results of Dickey-Fuller Test:'
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
            dfoutput['Critical Value (%s)'%key] = value
        print dfoutput
    

    def computeCorrelation(ts_log_diff,lags,func):    
        '''Method to calculate the ACF/PACF. func = 0 --> ACF & func = 1 --> PACF
        ACF is applied to compute MA value'''
        if(func == 0):
            lag_acf = acf(ts_log_diff, nlags=lags)
            return lag_acf
        if(func == 1):
            lag_pacf = pacf(ts_log_diff, nlags=lags, method='ols')
            return lag_pacf
            
    ############################# Plot functions. #################

    def plotGraph(ts_log_diff,func,title):
        '''Method to plot the graph of ACF and PACF depending on the value of dunc'''        
        plt.subplot(121) 
        #plt.plot(lag_acf)
        plt.plot(func)
        plt.axhline(y=0,linestyle='--',color='gray')
        plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
        plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
        #plt.title('Autocorrelation Function')
        plt.title(title)
        plt.show()

    def plotARIMAPredictions(ts,best_predictions_ARIMA):
        print best_predictions_ARIMA.head(10)
        #print p, q
        plt.plot(ts, color='blue')
        plt.plot(best_predictions_ARIMA, color='green')
        #plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
        plt.title('RMSE: %.4f'% mean_absolute_error(ts, best_predictions_ARIMA))
        plt.show()


############################# Model application and results function #################

    def predictPrice(self, p, q, fileName):
        mae, predictions_ARIMA = None, None
        try:
            data = readFile(fileName)
            ts,ts_log,ts_log_diff = stationarizeData(data)
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

############################# Main function that is called from outside. #################

    def applyARIMAModel(self, fileName):
        '''This function reads data from the given file, applies model, computes
        and returns the mean absolute error , predictions and p,q terms.'''
        minMae = 9999
        for i in xrange(1,6):
            for j in xrange(1,5):
                mae, predictions_ARIMA = predictPrice(i, j, fileName)
                if mae and not predictions_ARIMA.empty and mae < minMae:
                    minMae = mae
                    p, q = i, j
                    best_predictions_ARIMA = predictions_ARIMA
        return minMae, best_predictions_ARIMA



