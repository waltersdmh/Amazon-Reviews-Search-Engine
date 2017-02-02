import nltk
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import os
import pager


def inputFileToList(url):
    reviewList = pager.getReviewPages(url)
    return reviewList

def printLine(lineNo):
	thisList = inputFileToList()
	print(thisList[lineNo]);


class Review:

	def __init__(self, revId, revBody, revWeight):
		self.revId = revId
		self.revBody = revBody	
		self.revWeight = revWeight
		
	def printReview(self):
		print(self.revId)
		print(self.revBody + "\n")


def createRevArray(url):
    counter = 0
    reviewList = inputFileToList(url) # get all the reviews into one long list of strings
    reviewArray = []
    print(len(reviewList))
    for item in reviewList: # for each review string in review list
        revId = counter ## rev id
    #    revParts = [] # temp array for review components
    #    revParts.append(str(counter)) # at the id as the first component
     #   tempString = reviewList[counter] # select the next review from the list
        #tempString = "".join(tempString)#convert the reivew to a string (it was stored as a list with 1 element)
   #     revParts.append(tempString) 
        rev = Review(revId, reviewList[counter], 0)
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
def searchA():
	keyword = input("Search for: ")
	results = []
	print("searching for: ")
	print(keyword)
	for rev in reviewArray:
		review = rev.revBody
		if keyword in review:
			print("found match")
			results.append(rev)		
	return results

	
			
def searchB():
    keyword = input("Search for: ")
    item = 0
    results = []
    keyword = getTokens(keyword)
    keyword = textFilter(keyword)
    keyword = stemTokens(keyword, stemmer)
    print("searching for: ")
    for word in keyword:
        print(word)
    for rev in reviewArray:
        review = rev.revBody
        review = getTokens(review)
        review = textFilter(review)
        review = stemTokens(review, stemmer)
        for item in range(len(keyword)):
            if keyword[item] in review:
                results.append(rev)
                print("found match")
            item = item + 1
        results = list(set(results))
            
	#	if str(keyword[0]) in review:
			
	#		results.append(rev)
			
    return results
			
	
def searchC():
	results = []
	keyword = input("Search for: ")
	keyword = getTokens(keyword)
	keyword = textFilter(keyword)
	keyword = stemTokens(keyword, stemmer)
	print("searching for: ")
	for word in keyword:
		print(word)
	for rev in reviewArray:
		review = rev.revBody
		review = getTokens(review)
		review = textFilter(review)
		review = stemTokens(review, stemmer)	
		fdist = FreqDist(review)
	#	rev.revWeight = fdist[str(keyword[0])]
		
		for word in keyword:
			#print(keyword.index(word))
			rev.revWeight = rev.revWeight + fdist[str(keyword[keyword.index(word)])]
	
	#print the top 3
	reviewArray.sort(key = lambda x: x.revWeight)
	results.append(reviewArray[-3])
	results.append(reviewArray[-2])
	results.append(reviewArray[-1])			
		
	return results
  
		



def userInput():
	results = []
	inputFunction = input("")
	if inputFunction == "search(a)":
		results = searchA()
		for review in results:
			reviews.printReview()
	elif inputFunction == "search(b)":
		results = searchB()
		for review in results:
			review.printReview()
	elif inputFunction == "search(c)":
		results = searchC()
		for review in results:
			review.printReview()
	else:
		print("invalid search criteria")
	input("press any key")
	main()


def main():
    os.system('mode con: cols=200 lines=60')
    print("Review Search Engine 1.0 \n")
    print("This program will search for reviews based on a keyword or phrase entered \n")
    print("Type search(function) to begin searching, where function = \n")
    print("a = standard keyword match search. results are based on order of occurence(the type used by amazon.com)")
    print("b = search a + Tokenization + filtering + stemming ")
    print("c = search b + frequency distribution")
    userInput()
	

		
url = "https://www.amazon.co.uk/Chelsea-Football-Club-Santa-Christmas/dp/B002X3E7C4/ref=sr_1_2?ie=UTF8&qid=1485994653&sr=8-2&keywords=chelsea+fc"
reviewArray = createRevArray(url)
main()


	
	
