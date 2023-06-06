from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField , SubmitField , ValidationError , IntegerField
from wtforms.validators import DataRequired, Email, EqualTo , Length


class RegisterForm(FlaskForm):
    def validate_name(form, field):
        if not field.data.isalpha():
            raise ValidationError("Name must contain only letters")

    full_name = StringField('name' , validators = [DataRequired() , validate_name , Length(min= 3) ])
    email = StringField('email' , validators=[DataRequired() , Email()])
    password = StringField('password' , validators=[DataRequired()  , Length(min= 8)])
    confirm_password = StringField('password' , validators=[DataRequired() , EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField('email' , validators= [DataRequired() , Email()])
    password = StringField('password' , validators= [DataRequired()])


class SearchForm(FlaskForm):
    searched = StringField('searched' , validators=[DataRequired()])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    comment = TextAreaField('comment' , validators= [DataRequired()])


class ContactForm(FlaskForm):
    

    def validate_name(form, field):
        if not field.data.isalpha():
            raise ValidationError("Name must contain only letters")
        
    name = StringField('name' , validators=[DataRequired()])
    email = StringField('email' , validators=[DataRequired() , Email()])
    subject = StringField('subject' , validators=[DataRequired()])
    message = TextAreaField('message'  ,validators= [DataRequired()])


class FavoriteForm(FlaskForm):
    product_id = IntegerField('product_id' , validators=[DataRequired()])
    user_id = IntegerField('user_id' , validators=[DataRequired()])
    submit = SubmitField("Submit")