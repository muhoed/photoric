from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, MultipleFileField

from photoric.modules.upload import photos


# upload form
class UploadButton(FlaskForm):
    """Images upload form"""
    photo = MultipleFileField("upload_images",
                              render_kw={'multiple': True,
                                         'onchange': 'this.form.submit()'},
                              validators=[
                                    FileAllowed(photos, message='Only files of valid image formats (i.e. .jpg, .jpeg, .png, .tiff etc.) \
                                    are allowed')
                              ]
    )

    submit = SubmitField('Add')

