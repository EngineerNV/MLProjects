#created by Ice Master Nick Dizzy Dawg 
# was made for reading in files and creating a test and training sets
#file must be in the same directory
# we are returning a list of paths 
import glob 
import random 
from math import floor
# this is for only using one folder
# returns training and testing list of paths 
def createSets( fold ): 
	trainPercent = .9#determines the split for the known and unkown sets 
	fileList = glob.glob(fold+"\*.txt")
	trainSize = floor(len(fileList)*trainPercent)
	trainSet = random.sample( set( fileList ),int( trainSize ) )
	for path in trainSet: # eliminatiing the trainSet from original
		fileList.remove(path)
	testSet = fileList
	return(trainSet, testSet,) #returning a tuple list

def readFolder(fold):
	fileList = glob.glob(fold+"\*.txt")
	return fileList
	
# this is will be if we need to use two seperate folders
# returns training and testing for both so we can set conditions  
# might not use this 
def multiFolderSets( fold1, fold2, fold3 ): 	
	trH,teH = createSets( fold1 )
	tr2M,te2M = createSets( fold2 )
	tr3J,te3J = createSets( fold3 )
	total_list = [len(trH)+len(teH), len(tr2M)+len(te2M), len(tr3J)+len(te3J)]
	return( trH, teH, tr2M, te2M, tr3J, te3J, total_list )	
# made to recieve the included and Unknown set to give you the strings for when they are seperate and together
#made for your token needs 
def strText( tr, te):
	strKnown = ''
	strUnk = ''
	for path in tr: 
		f = open(path,encoding='utf-8').read()
		f = f.replace('\n',' ')
		trash,temp = f.split(':',1)
		strKnown = strKnown + temp
	for path in te:
		f = open(path,encoding='utf-8').read()
		f = f.replace('\n',' ')
		trash,temp = f.split(':',1)
		strUnk = strUnk + temp 
	strTotal = strKnown + ' ' + strUnk 
	return (strKnown, strUnk, strTotal)
# this is different because it returns a list of strings rather than a single tuple of strings 
def disStrText( test ):
	strList = []
	for path in test: 
		f = open(path,encoding='utf-8').read()
		f = f.replace('\n',' ')
		trash,temp = f.split(':',1)
		strList.append(temp) 
	return strList