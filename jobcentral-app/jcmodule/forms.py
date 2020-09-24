from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    query = StringField('Enter keywords')
    city = StringField('Where?')
    submit = SubmitField('Search')
