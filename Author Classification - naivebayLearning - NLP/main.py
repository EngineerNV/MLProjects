import tokenizer as tk
import dictionary as dic
import fileGet as get
# tok = tk.makeTokens('Forget YOU stupid normies, vape: sugar-free you dig? I like smoking. I like wearing hats.')
# # print("Tokens: ", tok)

def main():
 	#fold1 = sys.argv[1]
 	#fold2 = sys.argv[2]
 	#fold3 = sys.argv[3]
 	#undist = sys.argv[4]
	
	#grabbing necessary folders
	ham = 'Hamilton'; mad = "Madison"; jay = "Jay" ; dis = 'Disputed'
	#ham = 'binH'; mad = "binM"; jay = "binJ" ; dis = 'binTest'
	hamInc,hamUnk,madInc,madUnk,jayInc,jayUnk,total_list= get.multiFolderSets(ham,mad,jay)
	disPaths = get.readFolder(dis) # we wont be doing a dicitionary for this
	
	#getting the strings for the files. The full of both unk and known, and the seperate known and unkown sets
	hamStrInc,hamStrUnk,hamFull = get.strText(hamInc,hamUnk)
	madStrInc,madStrUnk,madFull = get.strText(madInc,madUnk)
	jayStrInc,jayStrUnk,jayFull = get.strText(jayInc,jayUnk)
	disStrList = get.disStrText( disPaths );
	
	#Making tokens 
	#---------------------------------------
	
	#disputed
	disTokList = [tk.makeTokens(string) for string in disStrList] # creating list of tokens
	
	
	#hamilton
	hamTokInc = tk.makeTokens(hamStrInc)
	hamTokUnk = tk.makeTokens(hamStrUnk)
	hamTokFull = tk.makeTokens(hamFull)
	
	#madison
	madTokInc = tk.makeTokens(madStrInc)
	madTokUnk = tk.makeTokens(madStrUnk)
	madTokFull = tk.makeTokens(madFull)
	
	#jay (not jayz, the guy who cheated on his wife)
	jTokInc = tk.makeTokens(jayStrInc)
	jTokUnk = tk.makeTokens(jayStrUnk)
	jTokFull = tk.makeTokens(jayFull)
	#--------------------------------------------
	
	#initializing dictionary and getting the number of documents 
	articles = dic.initAuthorProb(total_list,ham,mad,jay) #this will be used for author probablity 
	dics = dic.initDictionary()
	
	#distributing Dics all around 
	hammy = dics[0]; maddy = dics[1]; jdog = dics[2]
	
	# getting the iterations of all the words 
	wordsHamInc = dic.getWordCount(hamTokInc)
	wordsHamUnk = dic.getWordCount(hamTokUnk)
	wordsMadInc = dic.getWordCount(madTokInc)
	wordsMadUnk = dic.getWordCount(madTokUnk)
	wordsJayInc = dic.getWordCount(jTokInc)
	wordsJayUnk = dic.getWordCount(jTokUnk)
	
	#filling the iteration data inside the dics
	hammy = dic.fillDictionary(wordsHamInc,hammy)
	maddy = dic.fillDictionary(wordsMadInc,maddy)
	jdog = dic.fillDictionary(wordsJayInc,jdog)
	
	#this function makes sure to fill zeros in all the dics that have dont have stuff the other dics have
	hammy,maddy,jdog = dic.addOtherWords(hammy,maddy,jdog)
	
	#adding the Unk probability to the set
	hammy = dic.addUnknowns(wordsHamUnk, hammy)
	maddy = dic.addUnknowns(wordsMadUnk, maddy)
	jdog = dic.addUnknowns(wordsJayUnk, jdog)
	
	#setting the prob
	jdog = dic.setProbability(jdog)
	hammy = dic.setProbability(hammy)
	maddy = dic.setProbability(maddy)
	#print("before Smoothing")
	#print("J:"+str(jdog )+"H:"+str(hammy )+"M:"+str(maddy))
	#print('---------')
	#performing the smoothing with the log 
	jdog = dic.performSmoothing(len(jTokFull),len(set(jTokFull)),jdog)
	hammy = dic.performSmoothing(len(hamTokFull),len(set(hamTokFull)),hammy)
	maddy = dic.performSmoothing(len(madTokFull),len(set(madTokFull)),maddy)
	#print("After Smoothing")
	print("J:"+str(jdog )+"H:"+str(hammy )+"M:"+str(maddy))
	# classification step
	for i in range( len(disPaths) ):
		name,value,resultList =dic.classifyProb( disTokList[i], articles, hammy, maddy, jdog, ham, mad, jay)
		print("The File: " +disPaths[i] + " is Written by "+ name +" with probability:" + str(value))
		print("Total Results (name,value):" + str(resultList))
		
if __name__ == "__main__":
	main()