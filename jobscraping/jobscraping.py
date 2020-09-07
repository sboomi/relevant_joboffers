from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

from bs4 import BeautifulSoup
import requests

URL = "https://www.indeed.fr/"
keyword_request = ["python", "r", "tensorflow"]

# Takes the URL from Indeed and sorts results by date
def get_request_url(url, keywords):
    return url + "/jobs?q=" + "+".join(keywords) + "&sort=date"

browser = webdriver.Firefox()
url_req = get_request_url(URL, keyword_request) 
print(f"Accessing {url_req}...")
browser.get(url_req)

try:
    page_scroll = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination")))
except:
    print("Error: couldn't find page footer")
    browser.quit()

browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

job_offers = browser.find_elements_by_css_selector("h2.title")

soup_list = []

for offer in job_offers:
    offer_url = offer.find_element_by_name('a')
    page_content = requests.get(offer_url.get_attribute("href")).content
    soup = BeautifulSoup(html_doc, "html.parser")
    print(f"{offer.find_element_by_name('h2').text} parsed!")
    soup_list.append(soup)



browser.quit()