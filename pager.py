# given a url, gets all the reviews for a product.


import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup, Comment
import time
import re
import random 
import threading

reviews = []
numPage = 0
asin = ""

   #threading 

def pageScraper():
    global numpage
    threadGap = int(numPage/4)
#    print(threading.current_thread().getName())
    if threading.current_thread().getName() == "t1":
        getPages(1, threadGap)
    elif threading.current_thread().getName() == "t2":
        getPages(threadGap + 1, threadGap * 2)
    elif threading.current_thread().getName() == "t3":
        getPages(((threadGap * 2) + 1), threadGap * 3)
    elif threading.current_thread().getName() == "t4":
        getPages(((threadGap * 3) + 1), numPage)




def getPages(beg, end):
    global asin
    global reviews
    duration = end - beg
    pageNum = 0
    for page in range(duration):
        print("Thread ", threading.current_thread().getName(), " is fetching", pageNum+beg)
        #print(pageNum+beg)
        req = urllib.request.Request(
        url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=" + str(pageNum + beg), 
        data=None, 
        headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, "html.parser")
        for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
            reviews.append(row.text)
        pageNum = pageNum + 1














#input: url of product page (initially amazon, then other websties)
#output: list of url's of the prodicts review page.

def getReviewPages(url):
    print("pager.getReviewPages started")
    global reviews
    reviews = []
    position = url.index("/dp/")+4
    global asin
    asin = url[position:position+10]
    req = urllib.request.Request(
    url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1", 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, "html.parser")
    
    #return the number of review pages. numPage = number of pages
    stringNum = str(soup.find_all('span', attrs={"class" : "a-size-medium totalReviewCount"}))
    global numPage
    numPage = ''.join(x for x in stringNum if x.isdigit())
    print("number of reviews:")
    print(numPage)
    print(type(numPage))
    numPage = int(numPage)
    numPage = numPage / 10
    numPage = round(numPage) + 1
    print("number of pages:")
    print(numPage)
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
    
    
   
   
   
