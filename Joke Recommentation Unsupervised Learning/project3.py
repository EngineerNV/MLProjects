import pandas as pan
import numpy as np
import math as m
import random as rand
import matplotlib.pyplot as plt
import sys

def readInput (filename):
	# Read the input data and convert to numpy:
	input_data = pan.read_csv(filename, header=None); input_data = input_data.to_numpy()

	return input_data

def initRatings (data, numFeat):
	# Initialize height and width of data matrix:
	height, width = data.shape

	# Initialize the feature matrix, X:
	theta = np.zeros((height, numFeat))
	
	# Generate random feature value between -0.1 and 0.1:
	for i in range(height):
		for j in range(numFeat):
			theta[i][j] = round(rand.uniform(-0.1,0.1), 3)

	return theta

def initFeatures (data, numFeat):
	# Initialize height and width of data matrix:
	height, width = data.shape

	# Initialize the feature matrix, X:
	X = np.zeros((width, numFeat))
	
	# Generate random feature value between -0.1 and 0.1:
	for i in range(width):
		for j in range(numFeat):
			X[i][j] = round(rand.uniform(-0.1,0.1), 3)

	return X

def gradientDescent (X, theta, data, lamb, learnRate, numFeat, error):
	# Initialize control variables and allocate X_k and theta_k
	height, width = data.shape
	# theta_k = theta
	# X_k = X
	sum_x = 0; sum_theta = 0; sumX_v = np.zeros((width,numFeat))
	
	# Loop through dataset, for rated jokes only, and repeat until convergence:
	for i in range(width):
		for j in range(height):
			if (data[j][i] < 99):
				sum_x = sum_x + (np.dot((np.dot(theta[j].T, X[i]) - data[j][i]), theta[j]) + lamb*X[i])
		#print(sum_x)
		sumX_v[i] = sum_x ; sum_x = 0
			# print(X)

	for j in range(height):
		for i in range(width):
			if (data[j][i] < 99):
				sum_theta = sum_theta + (np.dot((np.dot(theta[j].T, X[i]) - data[j][i]), X[i]) + lamb*theta[j])
		
		theta[j] = theta[j] - learnRate*(sum_theta); sum_theta = 0
			# print(theta)
			
	for i in range(width): 
		X[i] = X[i] - learnRate*(sumX_v[i])
	
	return (X, theta, error)

def squareMean (X, theta, data):
	# Get the height and width of the dataset:
	height, width = data.shape
	error_sum = 0

	# Loop through the dataset and accumulate a sum:
	for i in range(width):
		for j in range(height):
			if (data[j][i] < 99):
				error_sum = error_sum + np.power(np.dot(theta[j].T, X[i]) - data[j][i], 2)
	return error_sum

def prediction (X, theta, data):
	# Calculate the prediction of unrated jokes:
	height, width = data.shape
	for i in range(width):
		for j in range(height):
			if (data[j][i] == 99):
				data[j][i] = np.dot(theta[j].T, X[i])
				#print(data[j][i])
# python filename learnrate lamb numFeat iterations
def main ():
	# Set default values here:
	# conditions for arguments, EITHER GIVE THEM ALL or WE SET THEM!!!! WAKONDA!!! 
	if len(sys.argv)<6:
		filename = "testj.csv"
		learnRate = 0.005
		lamb = 0.001
		numFeat = 10
		iterations = 500
	else:
		filename = sys.argv[1]
		learnRate = float(sys.argv[2])
		lamb = float(sys.argv[3])
		numFeat = int(sys.argv[4])
		iterations = int(sys.argv[5]) 
	
	# Initialize error variable to 0:
	error = []

	# Read user arguments, if any:

	# Read the input data from csv file:
	data = readInput (filename)

	# Get the feature and ratings vectors, X & theta:
	X = initFeatures (data, numFeat)
	theta = initRatings (data, numFeat)

	# Use gradient descent on the X and theta vectors:
	for i in range (iterations):	
		X, theta, error = gradientDescent (X, theta, data, lamb, learnRate, numFeat, error)
		error.append(squareMean (X, theta, data))
	# print(error)
	#print(data[1][1])
	#print(np.dot(theta[1].T, X[1]))
	
	# Find the square mean value:
	
	# Make a prediction for any unrated joke:
	prediction(X, theta, data)
	# print(data)

	# Plot the data for Dr. Hayes, because she's a cool person who probably owns an English budgie or two:
	plt.plot(error)
	plt.title("ERROR: English Budgies cannot vape!"); plt.ylabel('Computed Error'); plt.xlabel('Iterations')
	plt.show()
	

if __name__ == "__main__":
	main()