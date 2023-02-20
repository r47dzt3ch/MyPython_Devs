# importing the libraries
from bs4 import BeautifulSoup
import requests
#creating a function to get the channel info
#https://www.youtube.com/channel/UCSs5XcyhykU4oVv16iPmAJQ
def getChannelInfo(channel_url):
    #getting the content from the url
    r = requests.get(channel_url)
    #creating a soup object
    soup = BeautifulSoup(r.content, 'html5lib')
    #finding meta tags with the channel info
    meta_tags = soup.find_all('meta', attrs = {'name':True})
    #creating a dictionary to store the channel info
    channel_info = {}
    #looping through the meta tags
    for tag in meta_tags:
        #storing the channel info in the dictionary
        channel_info[tag['name']] = tag['content']
    #returning the channel info
    return channel_info
#watch the video using the selinium library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver=webdriver.Edge()
def watchtheVideo(channel_url):
    driver.get(channel_url)
    time.sleep(2)
#testing the function
if __name__ == '__main__':
    channel_url = 'https://www.youtube.com/channel/UCSs5XcyhykU4oVv16iPmAJQ'
    print(getChannelInfo(channel_url))
    watchtheVideo(channel_url)


