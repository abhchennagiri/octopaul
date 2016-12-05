
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import math
import csv
from itertools import izip
from sklearn.metrics import mean_squared_error, mean_absolute_error

plotting = False
predictFuture = False

class MultilayerPerceptronModel():

    def __init__(self, train_size=0.67, look_back=10, \
        neuron_size=10, future_points=14):

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

############################# Model application and results functions #############################

    def applyModel(self, dataset):
        '''Create,fit and predict the Multilayer perceptron model with 1 of input layer, hidden layer, output layer.
        The hidden layer contains "neuron_size" number of neurons. (t+1)th prediction is done by the end 
        of this function call.'''

        train, test = self.splitDataInotTrainAndTest(dataset)
        trainX, trainY = self.createDataset(train)
        testX, testY = self.createDataset(test)
        
        model = Sequential()
        model.add(Dense(self.neuron_size, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_absolute_error', optimizer='adam')
        model.fit(trainX, trainY, nb_epoch=200, batch_size=10, verbose=0)

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

        
        trainY, trainPredict = self.convertInfNanToZero(trainY), self.convertInfNanToZero(trainPredict)
        testY, testPredict = self.convertInfNanToZero(testY), self.convertInfNanToZero(testPredict)

        trainScore = mean_absolute_error(trainY, trainPredict)
        testScore = mean_absolute_error(testY, testPredict)
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
        plt.plot(dataset)
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
            testPredict = model.predict(testX)        
        
        return testPredict


############################# Main function that is called from outside. #################
    def applyMLPmodel(self, fileName):
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
        





