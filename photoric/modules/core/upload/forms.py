from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from .upload import photos


class UploadForm(FlaskForm):
    """Images upload form"""
    photo = FileField(
        validators=[
            FileAllowed(photos, message='Only files of valid image formats (i.e. .jpg, .jpeg, .png, .tiff etc.) are allowed'),
            FileRequired('File is empty')
        ]
    )
    submit = SubmitField('Upload images!')
