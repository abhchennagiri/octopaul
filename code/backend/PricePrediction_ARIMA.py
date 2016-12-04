import sys
sys.path.insert(0, '../lib/models')
#from RNN_model import RNNModel
#from multilayer_perceptron_model import MultilayerPerceptronModel
from ARIMA_model import ARIMAModel

class PricePrediction():
	def applyPredictionModels(self, fileName):
		'''Apply different prrediction models and return the mean absolute error returned by models.'''
		#mlpModel = MultilayerPerceptronModel()
		#mlpErr = mlpModel.applyMLPmodel(fileName)

		#rnnModel = RNNModel()
		#rnnErr = rnnModel.applyRNNmodel(fileName)
                try:
                    arima = ARIMAModel()
                    arimaErr = arima.applyARIMAModel(fileName)

                    randomWalkErr, predictions = arima.predictPrice(0,0,fileName)
                except:
                    pass

		return randomWalkErr, arimaErr
