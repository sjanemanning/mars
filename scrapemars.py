from splinter import Browser
import requests
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

def scrape_mars_news():
    try: 

        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html

        newssoup = BeautifulSoup(html, 'html.parser')


        newstitle = newssoup.find('div', class_='content_title').get_text()
        newscontent = newssoup.find('div', class_="rollover_description_inner").get_text()
        
        mars_info['newstitle'] = newstitle
        mars_info['newscontent'] = newscontent

        return mars_info

    finally:

        browser.quit()


def scrape_mars_image():

    try: 

        browser = init_browser()

        
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        
        htmlimage = browser.html

        imgsoup = BeautifulSoup(htmlimage, 'html.parser')

        featured_image_url  = imgsoup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        main_url = 'https://www.jpl.nasa.gov'
        featured_image_url = main_url + featured_image_url

        featured_image_url

        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()


def scrape_mars_weather():

    try: 

        
        browser = init_browser()

        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)

       
        htmlweather = browser.html

        weathersoup = BeautifulSoup(htmlweather, 'html.parser')

        lasttweet = weathersoup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
        marsweathertweet = lasttweet.find('p', 'tweet-text').get_text()
        mars_info['marsweathertweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()

def scrape_mars_facts():

    url = 'http://space-facts.com/mars/'
    marsfacts = pd.read_html(url)
    marsdf = marsfacts[0]
    marsdf.columns = ['Facts', 'Mars Data', 'Earth Data']


    marsdf.set_index('Facts', inplace=True)

    data = marsdf.to_html()

    mars_info['marsfacts'] = data

    return mars_info


def scrape_mars_hemispheres():

    try: 

       
        browser = init_browser()

        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        html_hemispheres = browser.html

        hemisoup = BeautifulSoup(html_hemispheres, 'html.parser')

        items = hemisoup.find_all('div', class_='item')

        hemisphere_image_urls = []
        hemispheres_main_url = 'https://astrogeology.usgs.gov'


        for i in items: 
            
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            hemisoup = BeautifulSoup( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + hemisoup.find('img', class_='wide-image')['src']
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            

        hemisphere_image_urls

        mars_info['hempisphere_image_urls'] = hemisphere_image_urls



        return mars_info
    finally:

        browser.quit()