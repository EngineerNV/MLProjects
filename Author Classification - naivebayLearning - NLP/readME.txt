By Nick Vaughn and Zack Something 

writen in python 

NLTK - tool kit was used for this 
In order to use our modules you must install, pip install ntlk 
then open python interpreter and run the downloads by doing these lines

import nltk 
nltk.download('punkt')
nltk.download('stopwords')
____________________________________________

After the nltk is installed you should be able to run the main.py file 

By default it will look for folders named "Hamilton", "Jay", "Madison", "Disputed"

If you don't want to run these folders you can change the names by going to line 14
ham = 'Hamilton'; mad = "Madison"; jay = "Jay" ; dis = 'Disputed'

change the variable names to the folder names you want
I have a binary test set that is commented, you can uncomment it and switch it out 
ham = 'binH'; mad = "binM"; jay = "binJ" ; dis = 'binTest'

We have no input arguments for the main, instead use that line to determine your input values

Note on the results:

Running the binary code gives us the results that are intended and good classification
The bigger problems lie on running the full sets with Jay included
Every result is labeled as Jay for the disputed files because the probabilities are vaped out (really Nick??) 
from the word size. Less word size seems to give Jay better probabilities then the other sets. 
If we were to remove the Jay set and change the code for two dictionaries my Hypothesis is that
the Madison and Hamilton would have a better time classifying between the two. The file size always
gives an advantage to the other classifier. So in a perfect scenario I would have to change the files
to the same exact text size when running over the disputed results. Perhaps bring it down to meet the size
of the Jay set. One document of Hamilton is WAY LARGER than a Jay Document or multiple Jay docs. 

The hamilton and Madison results are closely neck to neck over the disputed (IGNORING THE JAY). They differ at most
by 1000. 

Implementation: 

The core of this code comes from the inputs and tokenization choices we've made. We decided to do a 1 Gram 
classifier and to stem every single word with the NLTK. The stemming allows us to count more for words that have
the same root. Also all of the stop words are removed from the text. This can be seen in tokenizer.py. 
We use logs to repersent probabilities. For the Unkowns we use a random 90percent split in the fileGet.py method
createSets(fold) for an included set and a Unknown set. The idea to see how ofter the offer uses words no one 
else uses out of the three authors. For each author proabilitiy we use the number of articles out of the total
known to determine the rates in which papers are published. We add all the log probabilities together to get 
our results and the highest number gives us the answer we are looking for.  
Here is an example of the smoothing in the dictionary.py file performSmoothing method author[gram] = m.log((author[gram] + (1/unique))/(total + 1))

Once data is tokenized, it passes through the following functions in dictionary.py, one of which was mentioned in the
latter paragraph. First, the tokens go through a getWordCount() function, this removes duplicates of words and indicates the
number of times a specific word is used. Then the word data is passed into the fillDictionary() function, where each word and the associated 
count are inserted into the dictionary. The addOtherWords() function is used after each author's dictionary is created and filled with their
known data set. The known words from each author are added to the other two dictionaries with a count of zero. The unknown data, mentioned
before, gets added to each respective dictionary in addUnknowns(). If a word already exists in the dictionary, the counter for that word
is incremented by one. setProbability() goes through a single dictionary and divides the word count by the total number of words in
said dictionary. Lastly, performSmoothing() smoothes the dataset and takes the natural log to prevent underflow. Once training has occured,
classifyProb() classifies an author to a file through the word probabilities and author probabilities calculated with the training set.
Each author has an "author" probability. This is an additional probability of Hamilton, Madison, or Jay authoring an article based on the total
number of articles they have written. This probability is used in the classifyProb() function.

Actually running code:
python3 main.py 