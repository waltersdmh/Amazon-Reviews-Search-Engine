import nltk
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import os
import pager
import json

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

	
#traditional -in order of occurance - search used by amazon
#input keyword or phrase
def searchA(keyword):
	results = []
	for rev in reviewArray:
		review = rev.revBody
		if keyword in review:
			print("found match")
			results.append(rev)		
	return results

	
# Search A + language processing techniques but no ordering			
def searchB(keyword):
	results = []
	keyword = getTokens(keyword)
	keyword = textFilter(keyword)
	keyword = stemTokens(keyword, stemmer)
	# print("searching for: ")
	# for word in keyword:
	# 	print(word)
	for rev in reviewArray:
		review = rev.revBody
		review = getTokens(review)
		review = textFilter(review)
		review = stemTokens(review, stemmer)
		if all((w in review for w in keyword)):
			results.append(rev)
			print("found match")			
	return results
	
#Search C - full searching tool with relative frequency distribution applied
#input: key-terms, list of reviews, long review preference(boolean)
#output: ordered list of reviews. 			
def searchC(keywords, reviewArray, lenSet):
	results = []
	#format key-terms
	keyword = keywords
	keyword = getTokens(keyword)
	keyword = textFilter(keyword)
	keyword = stemTokens(keyword, stemmer)
	resetWeight(reviewArray)
	numReviews = len(reviewArray)
	for rev in reviewArray:
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
	results.sort(key = lambda x: x.revWeight)
	results.reverse() #reverse results, higher weighting first.
	return results

#clear rev.weight values
def resetWeight(reviews):
	for rev in reviews:
		rev.revWeight = 0;

#input: results, client identifier
#output: JSON file - list of reviews to send to client
def r2json(results, clientCode):
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
	
	
	r2json(results, clientCode)




	
	
