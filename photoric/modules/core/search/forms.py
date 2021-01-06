from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class SimpleSearch(FlaskForm):
    """Search form for top-menu"""
    text = StringField(
        'Search',
        validators=[Length(min=3, message='Search string must be at least 3 symbols long')],
        render_kw={"placeholder": "Words divided by spaces, commas or semicolons"}
    )
    submit = SubmitField('Search')
