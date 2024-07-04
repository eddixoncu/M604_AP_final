from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class OwnerForm(FlaskForm):
    document_number = StringField('document_number', validators=[DataRequired()]) 
    name = StringField('name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])    
    register = SubmitField('Submit')


class VehicleForm(FlaskForm):
    plate = StringField('plate', validators=[DataRequired()])
    owners = SelectField(u'Owners')
    change_owner = SubmitField('Change Owner')
