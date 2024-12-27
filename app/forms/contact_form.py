from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?1?\d{9,15}$', message="Please enter a valid international phone number (e.g., +97412345678)")
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ]) 