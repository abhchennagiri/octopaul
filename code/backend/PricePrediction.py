import sys
sys.path.insert(0, '../lib/models')
from RNN_model import RNNModel
from multilayer_perceptron_model import MultilayerPerceptronModel
from ARIMA_model import ARIMAModel

class PricePrediction():
	def applyPredictionModels(self, fileName):
		'''Apply different prrediction models and return the mean absolute error returned by models.'''
		arima = ARIMAModel()
		arimaErr, _ = arima.applyARIMAModel(fileName)

		randomWalkErr, _ = arima.predictPrice(0,0,fileName)

		mlpModel = MultilayerPerceptronModel()
		mlpErr = mlpModel.applyMLPmodel(fileName)

		rnnModel = RNNModel()
		rnnErr = rnnModel.applyRNNmodel(fileName)

		return randomWalkErr, arimaErr, mlpErr, rnnErr