from flask import render_template, url_for, redirect, flash, request
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from jcmodule import app, mongo, searchbar_model
from jcmodule.forms import SearchForm


@app.route('/')
@app.route("/main", methods=['GET', 'POST'])
def main_menu():
    """
    Show the main front page with the search bar, and latest job offers

    :return: The `main.html` page
    """
    latest_jobs = mongo.db.data.find().limit(10)
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit():
        keywords = form.query.data if hasattr(form.query, 'data') else ""
        city = form.query.city if hasattr(form.query, 'city') else ""
        return redirect((url_for('get_results', keywords=keywords, city=city)))
    return render_template("main.html", latest_jobs=latest_jobs, form=form)


@app.route('/results')
def get_results():
    """

    The function takes the query result and generates a page with all the results available.
    It gets the TF-IDF model and uses cosine similarity on the keywords request, in a way that it returns
    the most relevant results, which is then sent back in an ID

    For the city, it performs a simple regex search on the adress.

    :return: the results page if the query isn't empty, otherwise the main page
    """
    keywords = request.args.get("keywords")
    city = request.args.get("city")
    if not keywords and not city:
        flash('Hmm... Your query is empty...', 'info')
        return render_template('results.html', results=mongo.db.data.find().limit(10))
    else:
        offer_request = {}
        if keywords:
            keywords = re.split(r'\W', keywords.lower())
            keyword_vector = searchbar_model["model"].transform(keywords)
            cos_d = cosine_similarity(keyword_vector, searchbar_model["X"])
            simlist = cos_d[0]
            get_ids = [searchbar_model["y"][i] for i in np.argsort(simlist)[::-1]]
            offer_request["_id"] = {"$in": get_ids}
    if city:
        offer_request["city"] = {"$regex": city,
                                 "$options": 'i'}
    results = mongo.db.data.find(offer_request)
    flash(f'Success!! Returned {results.count()}...', 'success')
    return render_template('results.html', results=results)


@app.route("/offer/<string:offer_id>")
def show_offer(offer_id):
    """
    Takes the ID of an offer in the database and shows the information

    :param offer_id: :type string: The ID of the offer in the database
    :return: a page with the offer ID and the description
    """
    offer = mongo.db.data.find_one_or_404({"_id": offer_id})
    return render_template('offer.html', title=offer["title"], offer=offer)
