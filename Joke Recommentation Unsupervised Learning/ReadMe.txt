READ ME, if you can

Created by Nick Vaughn and Zack Abuelhaj

This program was made to use a recommendation system, and show how accurate perdictions can be over
certain amounts of iterations. 
We use collaborative filtering
All of the code is implemented in python 3.6 or higher. 
All the imports you need to have to run this file 

import pandas as pan
import numpy as np
import matplotlib.pyplot as plt
#installing 
pip install pandas 
python -m pip install --user numpy matplotlib
 
Format for running the file 
You must have all the instances in the arguments or else we use the following defaults 
	filename = "testj.csv"
	learnRate = 0.005
	lamb = 0.001
	numFeat = 10
	iterations = 500 

Example:
python project3.py testj.csv .005 .001 10 10

There are two files in the folder for testing our Joke database
testJ.csv, which has a smaller enough size to run multiple iterations
jester.csv, which has a LARGE amount of information 

We noticed that a small learning rate is key to having good accuracy. Anything like .5 will skew the data 
keep that in mind when playing with the values
