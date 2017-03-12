import nltk
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import os
import pager
import json





def inputFileToList(url, keywords, type, rating):
    reviewList = pager.startGetPages(url, keywords, type, rating)
    #print(reviewList)
    return reviewList

def printLine(lineNo):
	thisList = inputFileToList()
	#print(thisList[lineNo]);


class Review:

	def __init__(self, revId, revBody, revWeight):
		self.revId = revId
		self.revBody = revBody	
		self.revWeight = revWeight
		
	def printReview(self):
		#print(self.revId)
		#print(self.revBody + "\n")
		print()


def createRevArray(url, keywords, type, rating):
	counter = 0
	reviewList = inputFileToList(url, keywords, type, rating) # get all the reviews into one long list of strings
	reviewArray = []
	#print(len(reviewList))
	for item in reviewList: # for each review string in review list
		revId = counter ## rev id
#    revParts = [] # temp array for review components
#    revParts.append(str(counter)) # at the id as the first component
#   tempString = reviewList[counter] # select the next review from the list
#tempString = "".join(tempString)#convert the reivew to a string (it was stored as a list with 1 element)
   #     revParts.append(tempString) 
		rev = Review(revId, reviewList[counter], 0.0)
		counter = counter + 1
		reviewArray.append(rev)
	return reviewArray
	



# input: str
# output: str (without punctuation, lower case, in a list form.
def getTokens(original): #http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html

    lowers = original.lower()
    #remove the punctuation using the character deletion step of translate
    transtable = {ord(c): None for c in string.punctuation}
    no_punctuation = lowers.translate(transtable)
    tokens = nltk.word_tokenize(no_punctuation)
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

#stemmed = stemTokens(filtered, stemmer)
#print(reviewArray[2].revBody)
#print("\n")
#for review in reviewArray:

#reviewArray[2].revBody = getTokens(reviewArray[2].revBody)
#reviewArray[2].revBody = stemTokens(reviewArray[2].revBody, stemmer)
#print(reviewArray[2].revBody)

#randoText = "i am going to the shop. hi hello. carry carrying box boxing type typing happy good"
#print(randoText)
#randoText = getTokens(randoText)
#randoText = textFilter(randoText)
#randoText = stemTokens(randoText, stemmer)
#print("\n")
#print(randoText)	


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

		

	#	if str(keyword[0]) in review:
			
	#		results.append(rev)
			
	return results
	
		
	
def searchC(keywords, reviewArray, lenSet):
	#print("Search C started")
	results = []
	keyword = keywords
	keyword = getTokens(keyword)
	keyword = textFilter(keyword)
	keyword = stemTokens(keyword, stemmer)
	resetWeight(reviewArray)
	numReviews = len(reviewArray)
	
	for rev in reviewArray:
		review = rev.revBody
		review = getTokens(review)
		review = textFilter(review)
		review = stemTokens(review, stemmer)
		fdist = FreqDist(review) 				#frequency distribution of the review
		for word in keyword:
			if lenSet == "0":
				length = len(review)+1
				rev.revWeight = (rev.revWeight + (float(fdist[str(word)])) / length)
			else:
				rev.revWeight = rev.revWeight + (float(fdist[str(word)]))
		results.append(rev)
			# tempWeight = float(fdist[str(word)])
			# if tempWeight == 0:
			# 	rev.revWeight = rev.revWeight + 0 
			# elif tempWeight == 1:
			# 	rev.revWeight = rev.revWeight + 1
			# elif tempWeight == 2:
			# 	rev.revWeight = rev.revWeight+ 2
			# elif tempWeight == 3:
			# 	rev.revWeight = rev.revWeight+ 3
			# elif tempWeight == 4:
			# 	rev.revWeight = rev.revWeight+ 4
			# else:
			# 	rev.revWeight = rev.revWeight+5
		
		# if all((w in review for w in keyword)):
		# 	rev.revWeight = rev.revWeight + 4
		# 
		# if " ".join(keywords) in rev.revBody:
		# 	rev.revWeight = rev.revWeight + 6
			
	#	rev.revWeight = fdist[str(keyword[0])]
	
		#if rev.revWeight > 0.5:
		
		
#  	#print the top 10




	results.sort(key = lambda x: x.revWeight)
	#remove where 0
	
	results.reverse()
	return results

def resetWeight(reviews):
	for rev in reviews:
		rev.revWeight = 0;

def r2json(results, clientCode):
	#print("r2json started. converting restults to json")
	if len(results) == 0:
		rev = Review(1,"Sorry, but no reviews were found for that query. Try widening your search critera.", 1)
		results.append(rev)
		
	lines = []
	simplejson = json
	f = open(clientCode+".txt","w")
	for rev in results:
		lines.append(rev.revBody)
	#for item in lines:
		#print(item)
	simplejson.dump(lines, f)
	f.close()



# def userInput():
# 	results = []
# 	inputFunction = input("")
# 	if inputFunction == "search(a)":
# 		keyword = input("Search for: ")
# 		results = searchA(keyword)
# 		for review in results:
# 			review.printReview()
# 		r2json(results)
# 	elif inputFunction == "search(b)":
# 		keyword = input("Search for: ")
# 		results = searchB(keyword)
# 		for review in results:
# 			review.printReview()
# 	elif inputFunction == "search(c)":
# 		keyword = input("Search for: ")
# 		results = searchC(keyword)
# 		for review in results:
# 			review.printReview()
# 			print(review.revWeight)
# 	else:
# 		print("invalid search criteria")
# 	input("press any key to continue")
# 	main()


#def main():
    # os.system('mode con: cols=200 lines=60')
    # print("Review Search Engine 1.0 \n")
    # print("This program will search for reviews based on a keyword or phrase entered \n")
    # print("Type search(function) to begin searching, where function = \n")
    # print("a = standard keyword match search. results are based on order of occurence(the type used by amazon.com)")
    # print("b = search a + Tokenization + filtering + stemming ")
    # print("c = search b + frequency distribution")
    # userInput()
    
			
	
def main(message, clientCode):
	args = message.split(",")
	keywords = args[0]
	url = args[1]
	rating = args[2]
	type = args[3]
	lenSet = args[4]
	
	print("Selected type: " + str(type))
	print("Selected ratings: " + str(rating))
	print(lenSet)
	
	# if url exists within server.urlarray / temp remove this
#	import server
#	num = server.searchNo
#	if url == server.currenturl: 	
#		results = searchC(keywords, server.serverReviewArray)
#		r2json(results)
#	server.currenturl = url	

	reviewArray = createRevArray(url, keywords, str(type), str(rating))
	#print(reviewArray)
#	server.serverReviewArray = reviewArray
	results = searchC(keywords, reviewArray, lenSet)
	r2json(results, clientCode)




	
	
