# given a url, gets all the reviews for a product.


import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup, Comment
import re


#url='http://www.amazon.in/product-reviews/B00CE2LUKQ/ref=cm_cr_pr_top_link_1?ie=UTF8&showViewpoints=0&sortBy=bySubmissionDateDescending'
#content = urllib.request.urlopen(url).read()
#soup = BeautifulSoup(content, "html.parser")
#for row in soup.find_all('div',attrs={"class" : "a-row review-data"}):
#	print (row.text)


#input: url of product page (initially amazon, then other websties)
#output: list of url's of the prodicts review page.

url = "https://www.amazon.co.uk/Kingston-Technology-Solid-State-Drive/dp/B00A1ZTZOG/ref=s9_wsim_gw_g147_i1_r?_encoding=UTF8&fpl=fresh&pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=&pf_rd_r=FDXWV14YR248B1WWH4YQ&pf_rd_t=36701&pf_rd_p=c6eda34d-0edd-4e41-934b-1a9ae4c15500&pf_rd_i=desktop" 

def getReviewPages(url):
    position = url.index("/dp/")+4
    num = []
    asin = url[position:position+10]
    
    revPageUrl = "https://www.amazon.co.uk/product-reviews/" + asin + "/ref=cm_cr_dp_see_all_btm?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent"
    
    
#    opener = urllib.request.build_opener()
#    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#    response = opener.open(revPageUrl)
#    html_contents = response.text 
#    print(html_contents)
    
    
    
	#print(asin) 
    
	#print(revPageUrl)
#    numberOfPages = urllib.request.urlopen(url).read()
    
    page = requests.get(revPageUrl)
    html_contents = page.text
#    print(html_contents)
    
    
    soup = BeautifulSoup(html_contents, "html.parser")
    for row in soup.find_all('span',attrs={"id" : "acrCustomerReviewText"}):
        print(row.text)
        num.append(row)
 #   num = str(num[0])
  #  numPage = ''.join(x for x in num if x.isdigit())
   # numPage = int(numPage) / 10
    #print(numPage)
            
    

	
    
    
    
    
def run():
    getReviewPages(url)


run()
