from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import pickle

filename = "jobcentral-app/searchbar_model"
tfidf_v = TfidfVectorizer()

client = MongoClient(
    "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w=majority")
db = client.jobOffers
clean_data = db.cleanData

corpus = {clean_offer["_id"]: clean_offer["cleanText"] for clean_offer in clean_data.find()}

X = tfidf_v.fit_transform(list(corpus.values()))
y = list(corpus.keys())

with open(filename, "wb") as file:
    pickle.dump({"model": tfidf_v,
                 "X": X,
                 "y": y}, file)