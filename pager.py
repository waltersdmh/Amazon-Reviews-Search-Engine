# pager.py
# given a url, gets all the reviews for a product.
# updated to use search terms to build an amazon search url, reducing wasted time fecthing un-needed reviews from ALL pages.


import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup, Comment
import time
import re
import random 
import threading
import re
from random import choice

reviews = []
numPage = 1
asin =""
keywords = ""


#threading
#4 threads current best performance. more resulted in too many CAPTCHA interruptions.
#allocate blocks of work for each thread here, and give them a name.  
def pageScraper(addType, addRating):
    global numpage
    threadGap = int(numPage/4)
    if numPage <= 1:
        if threading.current_thread().getName() == "t1":
            getPages(0, 1, addType, addRating)
    if threading.current_thread().getName() == "t1":
        getPages(1, threadGap, addType, addRating)
    elif threading.current_thread().getName() == "t2":
        getPages(threadGap + 1, threadGap * 2, addType, addRating)
    elif threading.current_thread().getName() == "t3":
        getPages(((threadGap * 2) + 1), threadGap * 3, addType, addRating)
    elif threading.current_thread().getName() == "t4":
        getPages(((threadGap * 3) + 1), numPage, addType, addRating)


#random URL headers obtained from https://github.com/galkan/tools/blob/master/others/programming/python/random-http-headers-urllib.py
def random_spoof():
    UAS = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)','Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1','Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01','Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)']
    return(choice(UAS))

#scrape amazon review pages for reviews via DIV: "a-row review-data"
def getPages(beg, end, addType, addRating):
    global asin
    global reviews
    global numPage
    duration = end - beg
    pageNum = 1
    if duration == 0:
        duration =1
    for page in range(duration):
        print("Thread ", threading.current_thread().getName(), " is fetching", pageNum+beg)
        req = urllib.request.Request(
        url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType="+addType+"&showViewpoints=1&sortBy=helpful&pageNumber=" + str(pageNum + beg) + addRating + "&filterByKeyword=" + keywords, 
        data=None, 
        headers={'User-Agent':random_spoof()
    })
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, "html.parser")
        for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
            reviews.append(row.text)
        pageNum = pageNum + 1




#input: url of product page 
#output: numPage (the total number of pages) and a call to pageScraper

def getReviewPages(url, searchTerms, addType, addRating):
    global keywords
    keywords = searchTerms.replace(" ","+") # keywords seperated by +. W
    print("Keyterms: " + keywords)
    global reviews #provide access the to global reviews var
    reviews = []
    position = 0
    position = url.index("ref=")-11
    global asin
    asin = url[position:position+10]
    req = urllib.request.Request(
    url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=" + addType + "&showViewpoints=1&sortBy=helpful&pageNumber=1"+ addRating + "&filterByKeyword=" + keywords, 
    data=None, 
    headers={'User-Agent':random_spoof()
        #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    })
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, "html.parser")
    stringNum = soup.find("div", id="cm_cr-review_list").find("div", class_="a-section a-spacing-medium").find("span", class_="a-size-base").text
    start = "of"
    end = "reviews"
    str(stringNum)
    global numPage
    numPage = re.search('%s(.*)%s' % (start, end), stringNum).group(1) #w
    numPage.replace(" ", "")
    numPage = "".join(c for c in numPage if c not in (','))
    numPage = int(numPage)/10
    numPage = int(numPage)
    print("Number of pages: "  + str(numPage))
    
    pageNum = 1
    
    t1 = threading.Thread(name = "t1", target=pageScraper,args=(addType, addRating))
    t2 = threading.Thread(name = "t2", target=pageScraper,args=(addType, addRating))
    t3 = threading.Thread(name = "t3", target=pageScraper,args=(addType, addRating))
    t4 = threading.Thread(name = "t4", target=pageScraper,args=(addType, addRating))
    
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    
    print("pager.getReviewPages finished")
    return reviews
    
   
#startGetPages
#input: url, searchTerms, type(verified), rating
#output: list of review bodies
#calls: getReviewPages
    
def startGetPages(url, searchTerms, type, rating):
    addType = ""
    addRating = ""    
    if str(type) == "1":
        addType = "all_reviews"
    else:
        addType = "avp_only_reviews"        
    nrating = str(rating)
    if nrating == "6":
        addRating = "&filterByStar=all_stars"
    elif nrating == "5":
        addRating = "&filterByStar=five_star"
    elif nrating == "4":
        addRating = "&filterByStar=four_star"
    elif nrating == "3":
        addRating = "&filterByStar=three_star"
    elif nrating == "2":
        addRating = "&filterByStar=two_star"
    elif nrating == "1":
        addRating = "&filterByStar=one_star"
    reviews = []
    for num in range(3):
        try:
            reviews = getReviewPages(url, searchTerms, addType, addRating)
            if len(reviews)>=1:
                break
        except Exception as e:
            print("CAPTCHA RETRY")
            print(str(e))
            time.sleep(random.randint(1,2))
            continue
    #print(len(reviews))
    return reviews
    
   
   
