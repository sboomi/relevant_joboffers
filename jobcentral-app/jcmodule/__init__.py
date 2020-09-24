from flask import Flask
from flask_pymongo import PyMongo
import pickle

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w" \
                          "=majority "
app.config["SECRET_KEY"] = '_22XnxI2rAVNGqwFf29I5UksyP5Mi_IpvFOSVGEBRhI'

mongo = PyMongo(app)

with open("jobcentral-app/jcmodule/searchbar_model", 'rb') as file:
    searchbar_model = pickle.load(file)

from jcmodule import routes