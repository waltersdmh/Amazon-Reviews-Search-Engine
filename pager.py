# given a url, gets all the reviews for a product.


import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup, Comment
import time
import re
import random 



#input: url of product page (initially amazon, then other websties)
#output: list of url's of the prodicts review page.

def getReviewPages(url):
    print("pager.getReviewPages started")
    reviews = []
    position = url.index("/dp/")+4
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
    numPage = ''.join(x for x in stringNum if x.isdigit())
    numPage = int(int(numPage) / 10)+1 #remove rounding errors. 
    pageNum = 1
    #for every page, get all reviews. #second delay. for testing purposes, change numPage to small number.
    for page in range(numPage):
        print("fetching page")
        print(pageNum)
        time.sleep(random.randrange(2))
        req = urllib.request.Request(
        url = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=" + str(pageNum), 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, "html.parser")
        for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
            reviews.append(row.text)
        pageNum = pageNum + 1
    print("pager.getReviewPages finished")
    return reviews
 #   print(*reviews, sep='\n')
 #   print(len(reviews))
    
    
   
   
   
