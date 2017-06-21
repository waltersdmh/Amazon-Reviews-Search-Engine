import nltk
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import os
import pager
import json
import threading

results = []

#input: url + filters + key-terms
#output: a list of reviews
def inputFileToList(url, keywords, type, rating):
	reviewList = pager.startGetPages(url, keywords, type, rating)
	return reviewList

#tester - print 
def printLine(lineNo):
	thisList = inputFileToList()

#class Review
#revBody = the review content
#revWeight = ordering variable
class Review:
	def __init__(self, revId, revBody, revWeight):
		self.revId = revId
		self.revBody = revBody	
		self.revWeight = revWeight
		
	def printReview(self):
		#print(self.revId)
		#print(self.revBody + "\n")
		print()

#input: urlm key-terms, type, rating
#output: a list of reviews (reviewArray)
def createRevArray(url, keywords, type, rating):
	counter = 0
	reviewList = inputFileToList(url, keywords, type, rating) # get all the reviews into one long list of strings
	reviewArray = []
	for item in reviewList: # for each review string in review list
		revId = counter ## rev id
		rev = Review(revId, reviewList[counter], 0.0)
		counter = counter + 1
		reviewArray.append(rev)
	return reviewArray
	

# input: string (key-term or review)
# output: tokens of string (lower case with puctuation removed. all items tokenised)
def getTokens(original): 
	lowers = original.lower() #lower case
	transtable = {ord(c): None for c in string.punctuation} #build punctuation
	no_punctuation = lowers.translate(transtable) #remove punctuation
	tokens = nltk.word_tokenize(no_punctuation) #token
	return tokens

from nltk.stem.porter import *
#tokens = getTokens(original)
#filtered = [w for w in tokens if not w in stopwords.words('english')]

# input list
# output list with stop words removed
def textFilter(original):
	filtered = [w for w in original if not w in stopwords.words('english')]
	return filtered
	
#input list
#output list with items stemmed to base(english dictionary)
def stemTokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed
	
#define the stemmer we are using. used in stemTokens
stemmer = PorterStemmer()

		

	
#Search C - full searching tool with relative frequency distribution applied
#input: key-terms, list of reviews, long review preference(boolean)
#output: ordered list of reviews. 			
def searchC(keywords, reviewArray, lenSet):
	global results
	
	#format key-terms
	keyword = keywords
	keyword = getTokens(keyword)
	keyword = textFilter(keyword)
	keyword = stemTokens(keyword, stemmer)
	resetWeight(reviewArray)
	numReviews = len(reviewArray)
	
	#threading start
	t1 = threading.Thread(name = "t1", target=sendThreads,args=(reviewArray, numReviews, keyword, lenSet))
	t2 = threading.Thread(name = "t2", target=sendThreads,args=(reviewArray, numReviews, keyword, lenSet))
	t3 = threading.Thread(name = "t3", target=sendThreads,args=(reviewArray, numReviews, keyword, lenSet))
	t4 = threading.Thread(name = "t4", target=sendThreads,args=(reviewArray, numReviews, keyword, lenSet))
	   
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	  
	
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	
	results.sort(key = lambda x: x.revWeight)
	results.reverse() #reverse results, higher weighting first.
	
	
	
def sendThreads(reviewArray, numReviews, keyword, lenSet): 
	threadGap = int(numReviews/4)

	if threading.current_thread().getName() == "t1":
		orderRev(reviewArray, keyword, lenSet, 0, threadGap * 1)
		
	elif threading.current_thread().getName() == "t2":
		orderRev(reviewArray, keyword, lenSet, (threadGap * 1 + 1), threadGap * 2)
		
	elif threading.current_thread().getName() == "t3":
		orderRev(reviewArray, keyword, lenSet, (threadGap * 2 + 1), threadGap * 3)
		
	elif threading.current_thread().getName() == "t4":
		orderRev(reviewArray, keyword, lenSet, (threadGap * 3 + 1), threadGap * 4)	
	
	
	
def orderRev(reviewArray, keyword, lenSet, start, end):	
	global results
	for rev in reviewArray[start:end]:
		review = rev.revBody
		#format review body
		review = getTokens(review)
		review = textFilter(review)
		review = stemTokens(review, stemmer)
		fdist = FreqDist(review) #frequency distribution of the review
		for word in keyword:
			if lenSet == "0": #user prefers concise reviews
				length = len(review)+1
				rev.revWeight = (rev.revWeight + (float(fdist[str(word)])) / length)
			else: #user prefer longer reviews
				rev.revWeight = rev.revWeight + (float(fdist[str(word)]))
		results.append(rev)
		

	



#clear rev.weight values
def resetWeight(reviews):
	for rev in reviews:
		rev.revWeight = 0;

#input: results, client identifier
#output: JSON file - list of reviews to send to client
def r2json(clientCode):
	global results
	if len(results) == 0:
		rev = Review(1,"Sorry, but no reviews were found for that query. Try widening your search critera.", 1)
		results.append(rev)		
	lines = []
	simplejson = json
	f = open(clientCode+".txt","w")
	for rev in results:
		lines.append(rev.revBody)
	simplejson.dump(lines, f)
	f.close()
	results = []
	
def printHello():
	print("hello from " + str(print(threading.current_thread().getName())))

#main method
#1. interpret message settings 
#2. create review array
#3. apply search c
#4. format to json s
def main(message, clientCode):
	
	
	args = message.split(",")
	keywords = args[0]
	
# filtering the search terms for more results.

	newKey = keywords.split()
	newKey2 = textFilter(newKey)
	newKey3 = " ".join(str(n) for n in newKey2)
	print("filtered input: " + newKey3)
	keywords = newKey3

	url = args[1]
	rating = args[2]
	type = args[3]
	lenSet = args[4]
	reviewArray = createRevArray(url, keywords, str(type), str(rating))
	

	results = searchC(keywords, reviewArray, lenSet)
	
	
	r2json(clientCode)




	
	
