from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
from geopy.geocoders import Nominatim

#Load Database with testuser (read + write permissions)
client = MongoClient("mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/joboffers?retryWrites=true&w=majority")
db = client.jobOffers
collection = db.data

#Load geolocator
geolocator = Nominatim(user_agent="joboffers")

#Using Indeed
URL = "https://www.indeed.fr/"
keyword_request = ["python", "r", "tensorflow"]
n_pages = 5

# Takes the URL from Indeed and sorts results by date
def get_request_url(url, keywords):
    return url + "/jobs?q=" + "+".join(keywords) + "&sort=date"

# Evaluates the frequency of a list of keywords and returns a dictionnary
def kw_freq(keywords,text):
    d_words = {keyword.lower(): 0 for keyword in keywords}
    for word in re.split(r'\W', text):
        if word.lower() in d_words:
            d_words[word.lower()] += 1
    return d_words

browser = webdriver.Firefox()
url_req = get_request_url(URL, keyword_request) 
print(f"Accessing {url_req}...")
browser.get(url_req)

for i in range(1,n_pages+1):
    try:
        page_scroll = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination")))
    except:
        print("Error: couldn't find page footer")
        browser.quit()

    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    
    try:
        job_offers = browser.find_elements_by_css_selector("h2.title")
    except:
        print("Something went wrong. Quitting...")
        browser.quit()

    for offer in job_offers:
        offer_doc = {}
        offer_url = offer.find_element_by_tag_name('a')
        url = offer_url.get_attribute("href")
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content, "html.parser")
        print(f"{url} parsed!")
        offer_doc['_id'] = "INDEED_"+url.split("fccid=")[-1].replace("&vjs=3","")
        offer_doc['url'] = url
        offer_doc['title'] = soup.title.text
        details = soup.find("div",class_="jobsearch-InlineCompanyRating")
        if details:
            offer_doc["company"] = details.select_one("div.icl-u-lg-mr--sm.icl-u-xs-mr--xs").text
            city = details.find_all(class_=False)[-1].text
            country_code = soup.select_one("html").get('lang')
            location = geolocator.geocode(city, country_codes=country_code)
            offer_doc['address'] = location.address
        offer_doc["description"] = soup.find("div",id="jobDescriptionText").prettify()
        offer_doc["job_type"] = soup.select_one("div.jobsearch-JobMetadataHeader-item").text if soup.select_one("div.jobsearch-JobMetadataHeader-item") else None
        offer_doc["keyword_frequency"] = kw_freq(keyword_request, soup.find("div",id="jobDescriptionText").text)
        
        try:
            post_id = collection.insert_one(offer_doc).inserted_id
        except:
            post_id = offer_doc["_id"]
            print(f"Replacing  {post_id}...")
            collection.replace_one({"_id": post_id},offer_doc)
        else:
            print(f"{post_id} inserted!")



    
    print(f"Accessing page {i+1}...")
    
    browser.get(url_req + f"&start={i*10}")
    


browser.quit()