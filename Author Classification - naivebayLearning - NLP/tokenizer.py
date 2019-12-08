from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def makeTokens(text):
	stop = stopwords.words('english')
	stem = PorterStemmer()
	tok = word_tokenize(text)
	tokens = [stem.stem(word.lower()) for word in tok if (word.isalpha() or '-' in word) and (word.lower() not in stop)]
	return tokens	
#test lines
#tok = makeTokens('Forget YOU stupid normies, vape: sugar-free you dig? I like smoking. I like wearing hats.')
#print(tok)