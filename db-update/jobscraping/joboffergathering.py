from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from geopy.geocoders import Nominatim

# Load Database with testuser (read + write permissions)
client = MongoClient(
    "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/joboffers?retryWrites=true&w=majority")
db = client.jobOffers
collection = db.data

# Load geolocator to normalize the address
geolocator = Nominatim(user_agent="joboffers")
browser = webdriver.Firefox()