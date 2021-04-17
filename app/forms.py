from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    """Csv upload form."""
    upload = FileField(
        'imacsvge',
        [FileRequired()]
    )
    submit = SubmitField('Submit')