import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import csv
from numpy import inf
from itertools import izip
scaler = MinMaxScaler(feature_range=(0, 1))

plotting = False
predictFuture = False

class RNNModel():

    def __init__(self, train_size=0.67, look_back=10, \
        neuron_size=4, future_points=14):

        self.train_size = train_size
        self.look_back = look_back
        self.neuron_size = neuron_size
        self.future_points = future_points

############################# Data pre-processing functions. #############################

    def readFile(self, fileName):
        '''This function reads the csv file which has first column as dates and 
         second column as prices into a DataFrame object and returns it.'''

        # load the dataset
        dataframe = pd.read_csv(fileName, usecols=[1], engine='python')
        dataset = dataframe.values
        dataset = dataset.astype('float32')

        # normalize the dataset
        dataset = scaler.fit_transform(dataset)
        return dataset


    def splitDataInotTrainAndTest(self, dataset):
        '''This function splits data into train and test sets.'''

        train_size = int(len(dataset) * self.train_size)
        test_size = len(dataset) - train_size
        train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
        return train, test

    
    def createDataset(self, dataset):
        '''Convert an array of values into a dataset matrix; each row will contain look_back 
        number of values. Reshape data into numpy array of data[i to loop_back], data[t+1]'''
        dataX, dataY = [], []
        look_back = self.look_back
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)


    def reshapeData(self, data):
        # reshape input to be [samples, time steps, features]
        data = np.reshape(data, (data.shape[0], 1, data.shape[1]))
        return data


############################# Model application and results functions #############################

    def applyModel(self, dataset):
        '''Create,fit and predict the LSTM network with 1 of input layer, hidden layer, output layer.
        The hidden layer contains "neuron_size" number of neurons. (t+1)th prediction is done by the end 
        of this function call.'''

        train, test = self.splitDataInotTrainAndTest(dataset)
        trainX, trainY = self.createDataset(train)
        testX, testY = self.createDataset(test)
        
        model = Sequential()
        model.add(LSTM(self.neuron_size, input_dim=self.look_back))
        model.add(Dense(1))
        model.compile(loss='mean_absolute_error', optimizer='adam')

        #reshape the datasets from [samples, features] format to [samples, time steps, features].
        trainX = self.reshapeData(trainX)
        testX = self.reshapeData(testX)
        model.fit(trainX, trainY, nb_epoch=20, batch_size=1, verbose=0)

        # make predictions
        trainPredict = model.predict(trainX, batch_size=10)
        testPredict = model.predict(testX, batch_size=10)
        return trainPredict, testPredict, trainY, testY

    def convertInfNanToZero(self, array):
        array[array == -inf] = 0
        array[array == inf] = 0
        array[np.isnan(array)] = 0
        return array


    def computeError(self, trainPredict, testPredict, trainY, testY):
        '''Compute the mean absolute error for predicted values of both training and testing set.'''

        # invert predictions to original scale
        trainPredict = scaler.inverse_transform(trainPredict)
        trainY = scaler.inverse_transform([trainY])
        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])

        trainY, trainPredict = self.convertInfNanToZero(trainY), self.convertInfNanToZero(trainPredict)
        testY, testPredict = self.convertInfNanToZero(testY), self.convertInfNanToZero(testPredict)

        # calculate mean_absolute_error
        trainScore = mean_absolute_error(trainY[0], trainPredict[:,0])
        testScore = mean_absolute_error(testY[0], testPredict[:,0])
        return trainScore, testScore


    def plotGraph(self, dataset, trainPredict, testPredict):
        '''Plot the graph of original data vs predicted data for train and test.'''

        # shift train predictions for plotting
        trainPredictPlot = np.empty_like(dataset)
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
        # shift test predictions for plotting
        testPredictPlot = np.empty_like(dataset)
        testPredictPlot[:, :] = np.nan
        testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
        # plot baseline and predictions
        plt.plot(scaler.inverse_transform(dataset))
        plt.plot(trainPredictPlot)
        plt.plot(testPredictPlot)
        plt.show()


    def predictFuturePrices(self, dataset, testPredict):
        '''Predict the future prices for next futurePoints of values and return the array.
        Each predicted value is considered as a datapoint for next value to be predicted.'''

        def get_data(dataset):
            look_back = self.look_back
            dataX, dataY = [], []
            for i in range(len(dataset)-look_back-1):
                tmp1 = dataset[i:(i+look_back)] 
                dataX.append(tmp1)
                tmp2 = dataset[i + look_back] 
                dataY.append(tmp2)
            return np.array(dataX), np.array(dataY)

        _, test = self.splitDataInotTrainAndTest(dataset)
        for i in xrange(futurePoints):
            test = np.append(test, testPredict[-1])
            testX, testY = get_data(test, look_back)
            testX = reshape_data(testX)
            testPredict = model.predict(testX)

        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])
        
        # with open("rnn_predict.csv", 'wb') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(izip(testY[0], testPredict))

        return testPredict
        


############################# Main function that is called from outside. #################
    def applyRNNmodel(self, fileName):
        '''This function reads data from the given file, applies model, computes
        and returns the mean absolute error of predicted prices.'''
        #try:
        dataset = self.readFile(fileName)
        trainPredict, testPredict, trainY, testY = self.applyModel(dataset)
        _, mae = self.computeError(trainPredict, testPredict, trainY, testY)
        if plotting:
            self.plotGraph(dataset, trainPredict, testPredict)
        if predictFuture:
            self.predictFuturePrices(dataset, testPredict)

        return mae
        # except:
        #     pass

