# Dictionary and Naive Bayes algorithm.
# Written by Zach Abuelhaj Spring 2019

# Import modules here:
import math as m

# Create seperate dictionary that is for each author based on
# numbers of articles written. [Hamilton, Madison, Jay]
def initAuthorProb (file_num,ha,ma,ja):
	articles = {}
	total = file_num[0] + file_num[1] + file_num[2]
	articles[ha] = file_num[0]/total
	articles[ma] = file_num[1]/total
	articles[ja] = file_num[2]/total
	return articles

# Function to initalize the dictionaries:
def initDictionary ():
	hammy = {}; maddy = {}; jdog = {}
	return [hammy, maddy, jdog]

# Need a function that creates list of words and their occurance:
def getWordCount (tokens):
	words = []; length = len(tokens)
	for i in range(length):
		if any(tokens[i] in s for s in words):			# Pretty inefficient, but sublists can be tricky. If we know the token is in the list, then find the sublist and accumulate the occurance.
			for sublist in words:
				if (tokens[i] in sublist):
					sublist[1] = sublist[1] + 1			# Hey, man. It works.
		else:
			words.append([tokens[i], 1])

	return words

# Function that searches dictionary and returns the key:
def search (author, word):
	for key, value in author.items():
		if word in key:
			return value
		else:
			return 0

# Function to insert words to the dictionary. Words will be enumerated and have 2 attributes.
# {'word1': 0.5], 'word2': 0.5]}, where the attributes are the word and the probability.
# The 'words' list should be the following structure: [['word1', 2], ['word2', 1], etc].
# Does not set the probability of a word as it goes along.
def fillDictionary (words, author):
	# Set the length based on the number of incoming words:
	length = len(words)

	# Loop through each word and add it to the dictionary:
	for i in range(length):
		gram = words[i][0]; count = words[i][1]
		author[gram] = count

	return author

# Function that adds additional words to one dictionary from another:
def addOtherWords (hamilton, madison, jay):
	# Add Hamilton words to Madison:
	for gram in hamilton:
		if gram not in madison:
			madison[gram] = 0
		if gram not in jay:
			jay[gram] = 0

	# Add Madision to Hamilton:
	for gram in madison:
		if gram not in hamilton:
			hamilton[gram] = 0
		if gram not in jay:
			jay[gram] = 0

	# Add Jay to Hamilton:
	for gram in jay:
		if gram not in hamilton:
			hamilton[gram] = 0
		if gram not in madison:
			madison[gram] = 0
	return (hamilton,madison,jay)
# Function that adds unknown values:
def addUnknowns (UNK, author):
	length = len(UNK)
	author['UNK'] = 0

	for i in range(length):
		gram = UNK[i][0]; count = UNK[i][1]
		if gram not in author:
			author['UNK'] = author['UNK'] + count
		else: 
			author[gram] = author[gram] + count

	return author

# Get the probability:
def setProbability (author):
	total = 0
	for gram in author:
		total = author[gram] + total
	for gram in author:
		author[gram] = author[gram]/total
	return author

# Perform smoothing, on the dataset: 
def performSmoothing (total, unique, author):
	for gram in author:
		author[gram] = m.log((author[gram] + (1/unique))/(total + 1))
	return author
	
def classifyProb( disTok,articles,hdic, mdic, jdic, ha, ma , ja ):
	hprob = 0 ; mprob = 0; jprob = 0 ; value= 0; name = ''
	print(hdic['UNK']) ; print(mdic['UNK']) ; print(jdic['UNK'])
	for word in disTok: # summation of all probabilities
		
		if word in hdic:
			
			hprob = hdic[word] + hprob
			print('hprob'+str(hprob)+word)
		else:
			hprob = hdic['UNK'] + hprob
			#print('hprob'+str(hprob)+word)
		if word in mdic:
			mprob = mdic[word] + mprob
			print('mprob'+str(mprob)+word)
		else:
			mprob = mdic['UNK'] + mprob
			#print('mprob'+str(mprob)+word)
		if word in jdic:
			jprob = jdic[word] + jprob
			print('jprob'+str(jprob)+word)
		else:
			jprob = jdic['UNK'] + jprob	
			#print('jprob'+str(jprob)+word)
	#adding the author probility 
	hprob = m.log(articles[ha]) + hprob
	mprob = m.log(articles[ma]) + mprob
	jprob = m.log(articles[ja]) + jprob
	if hprob > jprob and hprob > mprob:
		name = ha ; value = hprob
	elif mprob > jprob and mprob > hprob:
		name = ma; value = mprob
	else:
		name = ja; value = jprob
	
	return (name, value, [(ha,hprob),(ma,mprob),(ja,jprob)] )