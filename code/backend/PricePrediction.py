import sys
sys.path.insert(0, './models')
from RNN_model import RNNModel
from multilayer_perceptron_model import MultilayerPerceptronModel

class PricePrediction():
	def applyPredictionModels(self, fileName):
		'''Apply different prrediction models and return the mean absolute error returned by models.'''
		mlpModel = MultilayerPerceptronModel()
		mlpErr = mlpModel.applyMLPmodel(fileName)

		rnnModel = RNNModel()
		rnnErr = rnnModel.applyRNNmodel(fileName)

		return mlpErr, rnnErr