
import random
class neuron:
	# this class is used as a data sctructure to hold attributes
	# to intialize you just put in the number of weights you want to have for a single neuron
	# this class was made to be called multiple times to create multiple neurons
	# weights is a np vertical array that has each weight reperesenting a connection to another neuron
	def __init__(self,numWeight):
		self.weights = self.makeWeightArray(numWeight)
		self.input = 0 
		self.numWeight = numWeight

	#this method was not meant to be used outside of this class	
	def makeWeightArray(self,numWeight):
		rand = round(random.uniform(-1,1),3)
		weights = [rand]
		for i in range(1,numWeight):
			rand = round(random.uniform(-1,1),3)
			weights.append(rand)
		return weights
		
	def getOutput(self):
		return self.weights * self.input
