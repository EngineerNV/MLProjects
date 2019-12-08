# Credit Card Fraud Detection

To run: python3 neural_net.py trainCredit.csv testCredit.csv 28 0.5  

trainCredit.csv can be any training file. testCredit.csv can be any testing/verification file.  

28 was the number of neurons in each layer. Any number can be used, but it needs to be equal to the number of inputs in the trainging and testing data set.  

0.5 is the threshold; this could be changed, but 0.5 worked best for the credit card fraud dataset.  
  
we skip the 1st row and column to match the formating of the Fraud data.  
You must change the iterate variable in the main function to change iterations over a line in training  
If training on other files, might want to change .5 to .9  
