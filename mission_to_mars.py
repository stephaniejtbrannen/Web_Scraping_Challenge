from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pandas as pd
from selenium import webdriver
# %which chromedriver



def scrape_news():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)
        # URL of page to be scraped
        url = 'https://mars.nasa.gov/news/'

        browser.visit(url)
        time.sleep(3)
        
        # Create BeautifulSoup object; parse with 'lxml'
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')

        #news title
        news = news_soup.select(".grid_layout .list_text")[0]

        # article title
        news_title = news.a.text
        print(news_title)
        news_content = news.find("div", class_="article_teaser_body").text
        print(news_content)

        mars_news = {
                "news_title": news_title,
                "news_content": news_content
        }
        return mars_news

def scrape_featured_img ():
        

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)

        url = 'https://www.jpl.nasa.gov/spaceimages'
        browser.visit(url)

        browser.find_by_xpath('//*[@id="full_image"]').click()
        time.sleep(5)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_path = soup.find('img', class_='fancybox-image')


        featured_image_url = 'https://www.jpl.nasa.gov' + img_path.get('src')
        featured_image_url

        # feature_img = {
        #         "featured_image_url" : featured_image_url
        # }
        
        return featured_image_url

def scrape_weather():

        # URL of page to be scraped
        twitter_url = 'https://twitter.com/marswxreport?lang=en'

        # Retrieve page with the requests module
        twitter_response = requests.get(twitter_url)
        # Create BeautifulSoup object; parse with 'lxml'
        twitter_soup = BeautifulSoup(twitter_response.text, 'lxml')


        mars_weather_tweet = twitter_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
        mars_weather_string = mars_weather_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
        mars_weather = mars_weather_string.text
        mars_weather

        return mars_weather

def scrape_fun_fact():

        url = "https://space-facts.com/mars/"

        tables = pd.read_html(url)
        tables[0]

        type(tables)

        df = tables[0]
        df.columns = ["Fact", "Value"]
        df

        df.set_index("Fact", inplace = True)

        html_table = df.to_html()
        df.to_html('mars_facts.html')

        return html_table

def scrape_hemispere_images():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=True)
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        hemis_soup = BeautifulSoup(html, 'html.parser')

        i=0;
        hemisphere_image_urls = []

        for hemi_img in hemis_soup.find_all('div', class_='description'):
                i+=1;
                try:
                        img_xpath = '//*[@id="product-section"]/div[2]/div['+str(i)+']/div/a'
                        # img_results = browser.find_by_xpath(img_xpath)

                        button = browser.find_by_xpath(img_xpath).click()
                        html = browser.html
                        soup = BeautifulSoup(html, 'html.parser')
                        img_title = soup.find('h2', class_='title').text
                        img_path = soup.find('img', class_='wide-image')

                        hem_img_url = 'https://astrogeology.usgs.gov' + img_path.get('src')
                        browser.back()

                        if (img_title):
                                # print(img_title)
                                # print(hem_img_url)
                                # print(i)
                                hemisphere_image_urls.append({
                                                'title':img_title, 
                                                'img_url': hem_img_url
                                                })
                                        
                except ElementDoesNotExist:
                        print(e)
        return hemisphere_image_urls

