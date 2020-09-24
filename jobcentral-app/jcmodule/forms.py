from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    """
    Generates the search form
    """
    query = StringField('Enter keywords')
    city = StringField('Where?')
    submit = SubmitField('Search')
