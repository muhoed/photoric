from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import (
    InputRequired,
    Length,
    Regexp
)

from photoric.config.form_validators import name_exists


class CreateAlbumForm(FlaskForm):
    """User Sign-Up Form."""
    name = StringField(
        'Name:',
        validators=[InputRequired(message='Please enter album name'),
                    Length(min=3, message='Album name must be at least 3 symbols long'),
                    name_exists('album', message='Album with such name already exists')
                    ]
    )
    description = TextAreaField(
        'Description:',
        validators=[Length(max=250, message='250 symbols max')]
    )
    keywords = TextAreaField(
        'Keywords:',
        validators=[Length(max=300, message='300 symbols max'),
                    Regexp(r'(^[\w\s,;]*$)',
                           message='Only letters, numbers, spaces, underscore, /'
                                   'commas and semicolons are permitted')
                    ]
    )

    submit = SubmitField('Create')
