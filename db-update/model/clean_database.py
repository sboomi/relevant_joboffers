# Preprocessing all descriptions with a clean collection
from pymongo import MongoClient
from bs4 import BeautifulSoup
from langdetect import detect
import nltk
from nltk.corpus import stopwords

client = MongoClient(
    "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w=majority")
db = client.jobOffers

# Get stemmer
STEMMERS = {"fr": nltk.stem.snowball.FrenchStemmer(),
            "en": nltk.stem.snowball.EnglishStemmer(),
            "de": nltk.stem.snowball.GermanStemmer()}

offer_data = db.data
clean_data = db.cleanData


def get_stopwords(locale):
    sw = set()
    try:
        file = open(f"ressources/stopwords_{locale}.txt", "r", encoding="utf-8")
    except:
        print("Error, file doesn't exist... Creating stopword list...")
        sw = generate_stopword_list(locale)
    else:
        for line in file:
            sw.add(line.strip('\n'))
        file.close()
    return sw


def generate_stopword_list(locale):
    languages = {"en": "english", "fr": "french", "de": "german"}
    sw = stopwords.words(languages[locale])
    filename = f"stopwords_{locale}.txt"
    with open(f"ressources/{filename}","w", encoding="utf-8") as file:
        for word in sw:
            file.write(word + '\n')
    print(f"{filename} generated!")
    return sw


for offer in offer_data.find():
    clean_offer = {"_id": offer["_id"]}
    soup = BeautifulSoup(offer["description"])
    locale = detect(soup.get_text())

    clean_offer['language'] = locale
    lang_field = {"$set": {"descriptionLanguage": locale}}
    offer_data.update_one({"_id": offer["_id"]}, lang_field)

    try:
        stemmer = STEMMERS[locale]
    except:
        nltk.download()

    stop_words = get_stopwords(locale)
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    list_words = tokenizer.tokenize(soup.get_text().lower())
    clean_offer["cleanText"] = " ".join(tokenizer.tokenize(offer["title"].lower()) + [word for word in list_words if word not in stop_words])

    try:
        db.cleanData.insert_one(clean_offer)
    except:
        print(f"{offer['_id']} already exists")
    else:
        print(f"{offer['_id']} inserted!")