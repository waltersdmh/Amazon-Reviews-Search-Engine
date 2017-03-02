# given a url, gets all the reviews for a product.


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

def pageScraper():
    global numpage
    #print(numPage)
    threadGap = int(numPage/4)
    
    if numPage <= 1:
        if threading.current_thread().getName() == "t1":
            getPages(0, 1)
            
#    print(threading.current_thread().getName())
    if threading.current_thread().getName() == "t1":
        getPages(1, threadGap)
    elif threading.current_thread().getName() == "t2":
        getPages(threadGap + 1, threadGap * 2)
    elif threading.current_thread().getName() == "t3":
        getPages(((threadGap * 2) + 1), threadGap * 3)
    elif threading.current_thread().getName() == "t4":
        getPages(((threadGap * 3) + 1), numPage)



def random_spoof():
    UAS = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)','Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1','Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01','Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)']
    return(choice(UAS))







def getPages(beg, end):
    global asin
    global reviews
    global numPage
    duration = end - beg
    pageNum = 1
    
    
    if duration == 0:
        duration =1
    for page in range(duration):
        print("Thread ", threading.current_thread().getName(), " is fetching", pageNum+beg)
        #print(pageNum+beg)
        req = urllib.request.Request(
        url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=" + str(pageNum + beg) + "&filterByKeyword=" + keywords, 
        data=None, 
        headers={'User-Agent':random_spoof()
    })
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, "html.parser")
        for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
            reviews.append(row.text)
        pageNum = pageNum + 1







#input: url of product page (initially amazon, then other websties)
#output: list of url's of the prodicts review page.

def getReviewPages(url, searchTerms):
    global keywords
    keywords = searchTerms.replace(" ","+") # keywords seperated by +. W
    
    print("Keyterms: " + keywords)
    global reviews #provide access the to global reviews var
    reviews = []
    position = 0
    # try:
    #     position = url.index("/dp/")+4 #position in the url to get asin. need to rework
    #     print(position)
    # except ValueError:
    #     position = url.index("/product/")+9
    #     print(position)
    #print(position)
    
    position = url.index("ref=")-11
    #print(position)
    
    
    global asin
    asin = url[position:position+10]
    

    
    req = urllib.request.Request(
    url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1&filterByKeyword=" + keywords, 
    data=None, 
    headers={'User-Agent':random_spoof()
        #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    })
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, "html.parser")
        

#find out how many reviews there are on amazon, with the given keyterms   


    stringNum = soup.find("div", id="cm_cr-review_list").find("div", class_="a-section a-spacing-medium").find("span", class_="a-size-base").text
# print(stringNum) 
    start = "of"
    end = "reviews"
    str(stringNum)
    global numPage
    numPage = re.search('%s(.*)%s' % (start, end), stringNum).group(1) #w
    numPage.replace(" ", "")
    numPage = int(numPage)/10
    numPage = int(numPage)
    print("Number of pages: "  + str(numPage))
    
    
    
    
    #for row in soup.find_all('div',attrs={"class" : "a-section a-spacing-none review-views celwidget"}):
       # print(row.text)
    #print(soup)
    #for row in soup.find_all('li',attrs={"class" : "page-button"}):
    #    print(row.text)
    #    global numPage
    #    numPage = int(row.text)
    #    print(numPage)
   
    
    
    
    
 #   for row in soup.find_all('li',attrs={"class" : "page-button"}):
  #      print(row.text)
    
    
    
    #stringNum = soup.find("div", id="cm_cr-review_list").find("div", class_="a-section a-spacing-medium").find("span", class_="a-size-base").text
    #print(stringNum)
    
    

  #  numPage.replace(" ", "")
   # numPage = int(numPage)
    #print(stringNum)
   # global numPage
#    numPage = ''.join(x for x in stringNum if x.isdigit())
    
    
    
    

    



    #print("number of reviews:")
    #print(numPage)
    #print(type(numPage))
   # numPage = int(numPage)
   # numPage = numPage / 10
   # numPage = round(numPage) + 1
    #print("number of pages:")
    #print(numPage)
    pageNum = 1
    
    t1 = threading.Thread(name = "t1", target=pageScraper)
    t2 = threading.Thread(name = "t2", target=pageScraper)
    t3 = threading.Thread(name = "t3", target=pageScraper)
    t4 = threading.Thread(name = "t4", target=pageScraper)
    
    
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
    
    

        
        
        

    
    
# t1.join()
# t2.join()
# t3.join()
# t4.join()  

       
        
        
    #for every page, get all reviews. #second delay. for testing purposes, change numPage to small number.
    # for page in range(numPage):
    #     print("fetching page")
    #     print(pageNum)
    #   #  time.sleep(random.randrange(1))
    #     req = urllib.request.Request(
    #     url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=" + str(pageNum), 
    #     data=None, 
    #     headers={
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    #     })
    #     f = urllib.request.urlopen(req)
    #     soup = BeautifulSoup(f, "html.parser")
    #     for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
    #         reviews.append(row.text)
    #     pageNum = pageNum + 1
    #     
        
        
        
        
        
        
        

 #   print(*reviews, sep='\n')
 #   print(len(reviews))
    
    
def startGetPages(url, searchTerms):
    reviews = []
    for num in range(3):
        try:
            reviews = getReviewPages(url, searchTerms)
            if len(reviews)>=1:
                break
        except Exception as e:
            print("CAPTCHA RETRY")
            print(str(e))
            time.sleep(random.randint(1,2))
            continue
    print(len(reviews))
    return reviews
    
   
   
