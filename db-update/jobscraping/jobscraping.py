"""
Runs a script and scraps offers from the web, before directly integrating them inside MongoDB Atlas' cluster
"""
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
from geopy.geocoders import Nominatim

# Load Database with testuser (read + write permissions)
client = MongoClient(
    "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/joboffers?retryWrites=true&w=majority")
db = client.jobOffers
collection = db.data

# Load geolocator to normalize the address
geolocator = Nominatim(user_agent="joboffers")

# Using Indeed
URL = "https://www.indeed.fr/"
keyword_request = ["python", "r", "tensorflow"]  # Users can modify this variable
n_pages = 5  # Users can modify this variable


# Takes the URL from Indeed and sorts results by date
def get_request_url(url, keywords):
    """
    Takes Indeed's main URL and adds search keywords.
    Each result is sorted by date

    :param url: the URL to enter
    :param keywords: the keywords you wish to do a search upon
    :return: the url Selenium browser will query for you
    """
    return url + "/jobs?q=" + "+".join(keywords) + "&sort=date"


# Evaluates the frequency of a list of keywords and returns a dictionary
def kw_freq(keywords, text):
    """
    Takes a list of keywords and returns a dictionary counting
    the number of times each keyword appears inside the text

    :param keywords: the keywords to evaluate (list)
    :param text: the text in which we will
    :return: a dictionary of occurences
    """
    d_words = {keyword.lower(): 0 for keyword in keywords}
    for word in re.split(r'\W', text):
        if word.lower() in d_words:
            d_words[word.lower()] += 1
    return d_words


# Establishes the webdriver (Firefox by default)
browser = webdriver.Firefox()

url_req = get_request_url(URL, keyword_request)
print(f"Accessing {url_req}...")
browser.get(url_req)

# Iterate over the number of pages returned by the previous query
for i in range(1, n_pages + 1):
    try:
        # This will try to wait for the bottom of the page to load and thus get the whole DOM
        page_scroll = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination")))
    except(NoSuchElementException, TimeoutException):
        print("Error: couldn't find page footer")
        browser.quit()

    # Scrolls at the bottom of the page
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    try:
        # Gets each job offer within a web element
        job_offers = browser.find_elements_by_css_selector("h2.title")
    except NoSuchElementException:
        print("Something went wrong. Quitting...")
        browser.quit()

    for offer in job_offers:
        offer_doc = {}

        # Gets the URL of each job offer link
        # and retrieves the content using request
        offer_url = offer.find_element_by_tag_name('a')
        url = offer_url.get_attribute("href")
        page_content = requests.get(url).content

        # Gets the whole DOM of the offer and generates a soup object
        soup = BeautifulSoup(page_content, "html.parser")
        print(f"{url} parsed!")

        # Fills the dictionnary with the essential parameters
        offer_doc['_id'] = "INDEED_" + url.split("fccid=")[-1].replace("&vjs=3", "")
        offer_doc['url'] = url
        offer_doc['title'] = soup.title.text
        details = soup.find("div", class_="jobsearch-InlineCompanyRating")
        if details:
            offer_doc["company"] = details.select_one("div.icl-u-lg-mr--sm.icl-u-xs-mr--xs").text
            city = details.find_all(class_=False)[-1].text

            # Saves the locale_string (some offers might be in English but the job
            # location might be in a non-speaking English country
            country_code = soup.select_one("html").get('lang')
            offer_doc['locale_string'] = country_code

            # Uses locale_string to give the sometimes inaccurate geolocator more accuracy
            location = geolocator.geocode(city, country_codes=country_code)
            offer_doc['address'] = location.address

        # Only retrieves the HTML in the hopes it would print on the page
        # Note: sometimes the text gets mashed within the titles
        offer_doc["description"] = soup.find("div", id="jobDescriptionText").prettify()
        offer_doc["job_type"] = soup.select_one("div.jobsearch-JobMetadataHeader-item").text if soup.select_one(
            "div.jobsearch-JobMetadataHeader-item") else None
        offer_doc["keyword_frequency"] = kw_freq(keyword_request, soup.find("div", id="jobDescriptionText").text)

        # Inserts the post and if ID already exists, updates it
        try:
            post_id = collection.insert_one(offer_doc).inserted_id
        except DuplicateKeyError:
            post_id = offer_doc["_id"]
            print(f"Updating  {post_id}...")

            collection.update_one({"_id": post_id}, {"$set": offer_doc})
        else:
            print(f"{post_id} inserted!")

    print(f"Accessing page {i + 1}...")

    browser.get(url_req + f"&start={i * 10}")

# Closes script once it's done
browser.quit()
