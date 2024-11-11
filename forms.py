from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField, SelectMultipleField
from wtforms_alchemy import ModelForm
from models import Room
from flask_login import current_user

class SignUpForm(FlaskForm):
    username = StringField(label='User Name:')
    email = StringField(label='Email Adress:')
    password = PasswordField(label='Password:')
    submit = SubmitField(label='Submit')
    
class RoomForm(ModelForm):
    class Meta:
        model = Room
        only = ['topic', 'name', 'description']

        

    
    