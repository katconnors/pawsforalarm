# using flask-wtf documentation

import os
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, PasswordField, SelectField, DateField, TextAreaField, validators

class AnimalForm(FlaskForm):


    auth = PasswordField('* Authentication', validators=[validators.DataRequired(),validators.Regexp(os.environ["password"], message="Incorrect auth. token")])
    name = StringField('* Name', validators=[validators.DataRequired()])
    url = StringField('URL', validators=[validators.URL(),validators.Optional()])
    image = StringField('Image', validators=[validators.Optional()])
    type = StringField('* Type', validators=[validators.DataRequired()])
    gender = SelectField('Gender', validators=[validators.Optional()], choices=[(None,'-'),('female','female'),('male','male')])
    breed = StringField('* Breed', validators=[validators.DataRequired()])
    age = StringField('Age(text)', validators=[validators.Optional()])
    availabledate = DateField('Available Date', validators=[validators.Optional()])
    euthdate = DateField('Sched. Euth. Date', validators=[validators.Optional()])
    joindate = DateField('Join Date', validators=[validators.Optional()])
    groupstatus = SelectField('Group', validators=[validators.Optional()], choices=[('other','other'),('euthanasiadates','Has sched. euth. date'),('fosterrequests','Foster requested')])
    code = StringField('Adoption Code', validators=[validators.Optional()])
    weight = IntegerField('Weight(lbs)', validators=[validators.Optional()])
    bio = TextAreaField('Bio', validators=[validators.Optional()])

# class ShelterForm(FlaskForm):


