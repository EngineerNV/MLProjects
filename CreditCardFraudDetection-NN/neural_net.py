import csv
from neuron import neuron as Neuron
import numpy as np
import math as m
import sys
print ("Parakeets can't vape, they will die.")
#created by Nick Vaughn and Vaping Zack
#this class was made to be run with the main included at the bottom of the file after the class. 
#It uses the neuron.py file to store information about neurons inside of the list objects for the input layer and hidden layer
#this is a 1 input layer and 1 hidden layer implementation that gives out a single output for results 
#IMPORTANT: This was initiated for our Fraud Data, if you wanted to use this code for another set of csv data you must change the threshold value
#we recommend using a .5 threshold value for the fraud data, and .9 for more binary or other data
#it is important to note that this code by default SKIPS the 1st row of inputs
#and SKIPS the 1st column
#this is because we were adjusting for the format of the Fraud excel file
#when making custom data for this make sure to keep this is mind 
# Example Call: pyhton3 neural_net.py trainCredit.csv testCredit.csv 28(input#) .5(threshold#)
#ignore the print statements about Vape, those are for good luck
class neural_net:

	def __init__ (self, layers, size, train, test):
		self.width = layers
		self.length = size
		self.learnRate = .7
		
		#defining 0 as negative and 1 as positive from the credit card 
		self.falseNeg =0; self.falsePos = 0; self.trueNeg = 0; self.truePos = 0
		#strings for csv functions 
		self.trainFile = train
		self.testFile = test 
		# The neural net hidden layers and input layer, we
		# are only going to use one hidden layer for now:
		self.hidden_layer = []; self.neuron_list = []; self.output_correct = 0
		# Build the neural net template, which is an empty set of Neuron objects:
		self.buildNeuralNetTemplate ()
	# Master method that calls the other methods to train the neural network:
	def trainNeuralNet (self, read_row):
		
		# Initialize the Neuron Layers:
		self.initializeLayers (read_row,self.trainFile)

		# Finally, adjust the weight according to the output and error:
		self. adjustWeight ()


	# Build the neural network map/template ahead of time to
	# make processing multiple training sets easier:

	def buildNeuralNetTemplate (self):
		# Initialize the lists for the hidden layers and input nodes:
		self.neuron_list = [None] * self.length
		self.hidden_layer = [None] * self.length

		# Loop through each input element and create a neuron object:
		for i in range(self.length):
			self.neuron_list[i] = Neuron(self.length)
			self.neuron_list[i].input = 0
			self.hidden_layer[i] = Neuron(1)
			self.hidden_layer[i].input = 0
				
	# Initialize the neuron layers of the neural_net with a specified row:
	def initializeLayers (self, read_row,file):
		# Using the csv module, read the input dataset into the neuron objects:
		with open (file) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ',')
			# line_count is what actually controls how we read meaningful data for the neuron training:
			line_count = 0
			for row in csv_reader:
				# Want to ignore the fist row, because it doesn't have anything useful for the computer:
				if line_count != 0 and line_count == read_row:
					for col in range(len(row)):						
						# The first column is estraneous, so just iterate on meaninful data:
						if col != 0 and col <= self.length:
							# Read the input dataset into each corresponding neuron:
							self.neuron_list[col - 1].input = float(row[col])
						# Get the last element of the row, this is the correct output. This will be used later for the training set:
						elif col == (len (row) -1):
							self.output_correct = float(row[col])
							# Can break out of the for loop now:
							break
				# Update the line counter no matter what:
				line_count += 1
			# Calculate the prediction for the hidden layer nodes by summing the weight 
			# to the data given:
			for hidLay in self.hidden_layer:
				# Initialize the theta_T variable in the predicition equation:
				theta_T = 0
				# Calculate for the term by performing a summation throughout all the node inputs:
				for nerv in self.neuron_list:
					for weigh in nerv.weights:
						theta_T = weigh * nerv.input + theta_T
						
				# Solve for the prediction and save to the hidden_layer:
				hidLay.input = 1/(1 + m.exp (-theta_T))
				
	#this function was design to adjust the weights of both the hidden layer and the input layer		
	def adjustWeight(self):
		output = self.output()
		#creating error sigmas 	
		sigma_out = (self.output_correct-output)*output*(1-output)
		sigma_a = [nerv.weights[0]*sigma_out*nerv.input*(1-nerv.input) for nerv in self.hidden_layer]
		# sigma_a was created so that sigma_a(0) is for first node 
		#the weights of the input nodes in neuron_list are structured so that weights[0] is for a_0 in hidden layer 
		for nerv in self.neuron_list: # going through every input nerve 
			for i in range(len(nerv.weights)): # going through every single weight 
				#weight adjust input node formula
				nerv.weights[i] = self.learnRate*sigma_a[i]*nerv.input + nerv.weights[i]
		for nerv in self.hidden_layer: # going through every hidden layer nerve and update weights 
			nerv.weights[0] = self.learnRate*sigma_out*nerv.input + nerv.weights[0]	
	
			#getting the final layer that connects to the output
	#this passes back the sigmoid output forff the hidden layer nerves next to the output 
	def output(self):
		theta_T = 0
		for nerv in self.hidden_layer:
			for weigh in nerv.weights:
				theta_T = nerv.input*weigh + theta_T
		return (1/(1 + m.exp (-theta_T)))
	
	# meant to be called multiple times to test the answers a trained classifer runs, for each row of file
	def testNeuralNet(self,read_row,thresh):
		
		self.initializeLayers(read_row,self.testFile) # setting up layers
		#laying out the terms to make it easier to read
		correct_ans = self.output_correct
		print("output from System"+str(self.output()) + " output from correct ans=" + str(correct_ans) )
		outputIsCorrect = ( (thresh<= self.output() ) == correct_ans)
		outputIsNotCorrect = not outputIsCorrect
		#need to make 4 cases for each type of correct or incorrect classification of credit fraud
		if outputIsCorrect and (correct_ans == 1): # truePos 
			self.truePos = self.truePos + 1 
		elif outputIsCorrect and (correct_ans == 0): # trueNeg
			print("found true neg")
			self.trueNeg = self.trueNeg + 1
		elif outputIsNotCorrect and (correct_ans == 1): #falseNeg
			print("found False Neg")
			self.falseNeg = self.falseNeg + 1
		elif outputIsNotCorrect and (correct_ans == 0): #falsePos
			self.falsePos = self.falsePos + 1

	def printTestResults(self):
		print("HERE ARE THE RESULTS: SPONSORED BY ZACK's VAPE JUICE")
		print( "True Positives ="+ str(self.truePos) )
		print( "True Negatives ="+ str(self.trueNeg) )
		print( "False Positives ="+ str(self.falsePos) )
		print( "False Negatives ="+ str(self.falseNeg) )
		print("Average Accuracy =" + str( ( self.trueNeg+self.truePos )/( self.trueNeg+self.truePos+self.falseNeg+self.falsePos )  ))
		print("Precision = " + str ( self.truePos/(self.truePos + self.falsePos)))
		print("Recall = " + str (self.truePos/(self.truePos + self.falseNeg)))
#this was meant to print weights the nerves for both the input and hidden layer, made outside the class methods 
def printNerves(obj):
	print("--------------------------------------")
	print("Input Nerve Weights - each list a different nerve")
	for n in obj.neuron_list:
		print( )
		print(n.weights)
	print("Hidden Layer Weights ")
	for n in obj.hidden_layer:
		print( )
		print(n.weights)
	print("--------------------------------------")
#this is where the class object methods are called
def main():
	trainFile=sys.argv[1]
	testFile=sys.argv[2]
	inputNum = int(sys.argv[3])
	thresh = float(sys.argv[4]) 

	# Open the test and training files to get the size, the program will read a whole file.
	with open (trainFile) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ',')
			trainEnd = sum(1 for row in csv_reader)
	with open (testFile) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ',')
			testEnd = sum(1 for row in csv_reader)

	iterate = 1000 # adjust this if needed, good enough for fraud data, Careful when adjusting this higher could be slower. Adjust rows lower for faster speed
	#rows start and end for files, need to edit for other files 
	trainStart = 1; testStart = 1
	#calling on the Neural Net Class
	obj = neural_net(1,inputNum,trainFile,testFile)	#creating Net
	for i in range(trainStart,trainEnd):  #training net 
		print("Training Line: "+str(i))
		for j in range(iterate):
			obj.trainNeuralNet(i)
	print("Weights After Training")
	printNerves(obj)
	for i in range(testStart,testEnd):#testing net
		obj.testNeuralNet(i,thresh)
	obj.printTestResults()
			
if __name__ == "__main__":
    main()