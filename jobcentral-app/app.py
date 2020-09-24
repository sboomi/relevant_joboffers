from flask import Flask, render_template, url_for, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w" \
                          "=majority "
app.config["SECRET_KEY"] = '_22XnxI2rAVNGqwFf29I5UksyP5Mi_IpvFOSVGEBRhI'

mongo = PyMongo(app)

with open("jobcentral-app/searchbar_model", 'rb') as file:
    searchbar_model = pickle.load(file)


class SearchForm(FlaskForm):
    query = StringField('Enter keywords')
    city = StringField('Where?')
    submit = SubmitField('Search')


@app.route('/')
@app.route("/main", methods=['GET', 'POST'])
def main_menu():
    latest_jobs = mongo.db.data.find().limit(10)
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit():
        keywords = form.query.data if hasattr(form.query, 'data') else ""
        city = form.query.city if hasattr(form.query, 'city') else ""
        return redirect((url_for('get_results', keywords=keywords, city=city)))
    return render_template("main.html", latest_jobs=latest_jobs, form=form)


@app.route('/results')
def get_results():
    keywords = request.args.get("keywords")
    city = request.args.get("city")
    if not keywords and not city:
        flash('Hmm... Your query is empty...', 'info')
        return render_template('results.html', results=mongo.db.data.find().limit(10))
    keywords = re.split(r'\W', keywords)
    keyword_vector = searchbar_model["model"].transform(keywords)
    cos_d = cosine_similarity(keyword_vector, searchbar_model["X"])
    simlist = cos_d[0]
    get_ids = [searchbar_model["y"][i] for i in np.argsort(simlist)[::-1]]
    offer_request = {"_id": {"$in": get_ids}}
    if city:
        offer_request["city"] = {"$regex": city,
                                 "$options": 'i'}
    results = mongo.db.data.find(offer_request)
    flash(f'Success!! Returned {results.count()}...', 'success')
    return render_template('results.html', results=results)


@app.route("/offer/<string:offer_id>")
def show_offer(offer_id):
    offer = mongo.db.data.find_one_or_404({"_id": offer_id})
    return render_template('offer.html', title=offer["title"], offer=offer)


if __name__ == '__main__':
    app.run()
