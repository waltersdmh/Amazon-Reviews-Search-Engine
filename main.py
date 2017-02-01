import nltk
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import os


def inputFileToList():
	reviewList = []
	
	with open("inputMSREval/f_1.txt", 'r') as f:
		for line in f:
			reviewList.append(line.split("\n"))
		return reviewList
		

def printLine(lineNo):
	thisList = inputFileToList()
	print(thisList[lineNo]);


class Review:

	def __init__(self, revId, revDate, revProduct, revProductCode, revTitle, revBody, revWeight):
		self.revId = revId
		self.revDate = revDate
		self.revProduct = revProduct
		self.revProductCode = revProductCode
		self.revTitle = revTitle
		self.revBody = revBody	
		self.revWeight = revWeight
		
	def printReview(self):
		print(self.revId)
		print(self.revDate)
		print(self.revProduct)
		print(self.revProductCode)
		print(self.revTitle)
		print(self.revBody + "\n")


def createRevArray():
	counter = 0
	reviewList = inputFileToList() # get all the reviews into one long list of strings
##	print("reviewList length:") #test pass
##	print(len(reviewList)) #test pass
	reviewArray = []
	
	for item in reviewList: # for each review string in review list
	#	print(counter)
		revId = counter ## rev id
		revParts = [] # temp array for review components
		revParts.append(str(counter)) # at the id as the first component
			
	##	print("Printing revParts list:") #test pass
	##	for item in revParts: #testpass
	##		print(item)#testpass

		tempString = reviewList[counter] # select the next review from the list
			
	##	print(tempString) ##testpass

		tempString = "".join(tempString)#convert the reivew to a string (it was stored as a list with 1 element)
	#	print(tempString) #test pass
	#	print(type(tempString)) #type string 
	
		revParts.append((tempString.split("&&&"))) 
	#	for item in revParts:
	#		print(item)
	#		print("\n")	
		if len(revParts[1]) is 4:
			rev = Review(revParts[0], revParts[1][0], "No Phone" , revParts[1][1], revParts[1][2], revParts[1][3], 0)
		else:
			rev = Review(revParts[0], revParts[1][0], revParts[1][1], revParts[1][2], revParts[1][3], revParts[1][4], 0)
		counter = counter + 1
	#	rev.printReview()
		
		reviewArray.append(rev)
	return reviewArray
	
reviewArray = createRevArray() # create list of Reviews



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
	reviewArray = createRevArray()
	print("searching for: ")
	print(keyword)
	for rev in reviewArray:
		review = rev.revBody
		if keyword in review:
			print("found match")
			results.append(rev)		
	for review in results:
		print(review.printReview())
	print("Number of matching reviews: ")
	print(len(results))
	input("Press Enter to continue...")
	main()
	
			
def searchB():
	keyword = input("Search for: ")
	results = []
	reviewArray = createRevArray()
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
		if str(keyword[0]) in review:
			print("found match")
	#		results.append(rev)
			
	for review in results:
		print(review.printReview())
	print("Number of matching reviews: ")
	print(len(results))
		
	input("Press Enter to continue...")
	main()			
	
def searchC():
	keyword = input("Search for: ")
	reviewArray = createRevArray()
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
	reviewArray[-3].printReview()
	reviewArray[-2].printReview()
	reviewArray[-1].printReview()			
		
	input("Press Enter to continue...")
	main()	
			
def main():
	#os.system('mode con: cols=200 lines=20')
	print("Review Search Engine 1.0 \n")
	print("This program will search for reviews based on a keyword or phrase entered \n")
	print("Type search(function) to begin searching, where function = \n")
	print("a = standard keyword match search. results are based on order of occurence(the type used by amazon.com)")
	print("b = one word key search. Tokenization + filtering + stemming ")
	print("c = search b + frequency distribution")
	inputFunction = input("")
	if inputFunction == "search(a)":
		searchA()
	elif inputFunction == "search(b)":
		searchB()
	elif inputFunction == "search(c)":
		searchC()
		print("")
	else:
		print("invalid search criteria")
		main()
		



main()


	
	
