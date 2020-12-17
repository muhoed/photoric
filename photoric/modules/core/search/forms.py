from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SimpleSearch(FlaskForm):
    """Search form for top-menu"""
    text = StringField(
        'Search',
        validators=[]
    )
    submit = SubmitField('Search')
