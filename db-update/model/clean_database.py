"""
Preprocessing all descriptions with a clean collection, whose description has been filtered
"""
from pymongo import MongoClient
from bs4 import BeautifulSoup
from langdetect import detect
import nltk
from nltk.corpus import stopwords
from pymongo.errors import DuplicateKeyError

client = MongoClient(
    "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w=majority")
db = client.jobOffers

# Get stemmer
STEMMERS = {"fr": nltk.stem.snowball.FrenchStemmer(),
            "en": nltk.stem.snowball.EnglishStemmer(),
            "de": nltk.stem.snowball.GermanStemmer()}

# Instanciate databases
offer_data = db.data
clean_data = db.cleanData


def get_stopwords(locale_string):
    """
    Returns a set of stopwords from the desired language. It's fetching a list of stopwords under text format in the
    ressources folder, reads it, and returns a set.

    :param locale_string: :type string: The language of the stopword list
    :return: :type set: A set of stopwords
    """
    sw = set()
    try:
        file = open(f"db-update/ressources/stopwords_{locale_string}.txt", "r", encoding="utf-8")
    except FileNotFoundError:
        print("Error, file doesn't exist... Creating stopword list...")
        sw = generate_stopword_list(locale_string)
    else:
        for line in file:
            sw.add(line.strip('\n'))
        file.close()
    return sw


def generate_stopword_list(locale_string):
    """
    Generates a stopword list by default if this one doesn't exist in the ressources folder
    It takes the default stopword list from the NLTK package, registers a document and creates a set, which
    is the output argument.

    :param locale_string: :type string: The language of the stopword list
    :return: :type set: The new set of stopwords
    """
    languages = {"en": "english", "fr": "french", "de": "german"}
    sw = stopwords.words(languages[locale_string])
    filename = f"stopwords_{locale_string}.txt"
    with open(f"db-update/ressources/{filename}", "w", encoding="utf-8") as file:
        for word in sw:
            file.write(word + '\n')
    print(f"{filename} generated!")
    return sw


# Begin iteration over the whole raw collection
for offer in offer_data.find():
    # Instantiates a new document sharing the same ID
    clean_offer = {"_id": offer["_id"]}

    # Filters HTML if present
    soup = BeautifulSoup(offer["description"])
    locale = detect(soup.get_text())

    # Updates, if needed, the raw document to indicate the language
    clean_offer['language'] = locale
    lang_field = {"$set": {"descriptionLanguage": locale}}
    offer_data.update_one({"_id": offer["_id"]}, lang_field)

    # gets the stemmer
    try:
        stemmer = STEMMERS[locale]
    except KeyError:
        nltk.download()

    # generates the SW list & tokenizer
    stop_words = get_stopwords(locale)
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    # Cleans the text by excluding punctuation and stop words
    list_words = tokenizer.tokenize(soup.get_text().lower())
    clean_offer["cleanText"] = " ".join(
        tokenizer.tokenize(offer["title"].lower()) + [word for word in list_words if word not in stop_words])

    try:
        db.cleanData.insert_one(clean_offer)
    except DuplicateKeyError:
        print(f"{offer['_id']} already exists")
    else:
        print(f"{offer['_id']} inserted!")
