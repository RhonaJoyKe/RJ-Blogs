from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField, FileField,TextAreaField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Length, EqualTo
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
   
    submit = SubmitField('Submit')