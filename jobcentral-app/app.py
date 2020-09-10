from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo
import re

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w" \
                          "=majority "
app.config["SECRET_KEY"] = '_22XnxI2rAVNGqwFf29I5UksyP5Mi_IpvFOSVGEBRhI'

mongo = PyMongo(app)


class SearchForm(FlaskForm):
    query = StringField('Enter keywords')
    city = StringField('Where?')
    submit = SubmitField('Search')


@app.route('/')
@app.route("/main", methods=['GET', 'POST'])
def hello_world():
    latest_jobs = mongo.db.data.find().limit(10)
    form = SearchForm()
    if form.validate_on_submit():
        query = {"keywords": re.split(r'\W', form.query.data),
                 "city": form.query.city}
        return get_results(query)
    return render_template("main.html", latest_jobs=latest_jobs, form=form)


@app.route('/results')
def get_results(query):
    if not sum([1 if value else 0 for value in query.values()]):
        flash('Hmm... Your query is empty...', 'info')
        results = mongo.db.data.find().limit(10)
    # Insert earch engine here
    return render_template('results.html', results=results)


@app.route("/offer/<int:offer_id>")
def show_offer(offer_id):
    offer = mongo.db.data.find_one_or_404({"_id": offer_id})
    return render_template('offer.html', title=offer.title, offer=offer)


if __name__ == '__main__':
    app.run()
