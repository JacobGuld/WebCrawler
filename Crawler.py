from urllib import request
import requests
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser

frontier = []
prevVistedPages = []
currentDomain = ''

rp = RobotFileParser()

frontier.append('https://www.aau.dk/')

def availableForCrawling(url):
    global rp
    global currentDomain

    if '/' not in url or len(url) < 2:
        return False
    else:
       
        url = getDomain(url)
        
        rp.set_url(url)
        rp.read()
        return rp.can_fetch('*',url)

def getDomain(url):
    global currentDomain
    if 'https://' not in url:
        return currentDomain
    #print('Domain: ' + url)
    return 'https://'+ url.split('/')[2]+'/'

while len(frontier) > 0 and len(prevVistedPages) <= 1000:
    url = frontier.pop(0)
    currentDomain = getDomain(url)
    
    prevVistedPages.append(url)
    curPage = BeautifulSoup(requests.get(url).text, 'html.parser')
    subpages = curPage.find_all('a')
    print( 'Visited['+ str(len(prevVistedPages))+ '] '+ 'Subpages[' + str(len(subpages)) + '] ' + 'Domain['+ currentDomain + '] ' + 'Frontier[' + str(len(frontier)) + '] ' 'Crawling: ' + url)
    for page in subpages:
        pageUrl = page['href']
    
        if pageUrl.startswith('/'):
            pageUrl = pageUrl[1:]
            pageUrl = currentDomain + pageUrl
       
        if pageUrl not in prevVistedPages and availableForCrawling(pageUrl):
            frontier.append(pageUrl)

            


    







        
