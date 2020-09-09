from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://testuser:testuser@joboffers.jjm1u.mongodb.net/jobOffers?retryWrites=true&w" \
                          "=majority "
mongo = PyMongo(app)


class SearchForm(FlaskForm):
    query = StringField('Enter keywords')
    submit = SubmitField('Search')


@app.route('/')
@app.route("/main")
def hello_world():
    latest_jobs = mongo.db.data.find().limit(10)
    form = SearchForm()
    return render_template("main.html", latest_jobs=latest_jobs, form=form)


if __name__ == '__main__':
    app.run()
