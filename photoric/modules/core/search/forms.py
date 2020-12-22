from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SimpleSearch(FlaskForm):
    """Search form for top-menu"""
    text = StringField(
        'Search',
        validators=[],
        render_kw={"placeholder": "Search"}
    )
    submit = SubmitField('Search')
