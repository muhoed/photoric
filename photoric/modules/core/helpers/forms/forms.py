from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    InputRequired,
    Email,
    EqualTo,
    Length,
    Regexp
)


class SignupForm(FlaskForm):
    """User Sign-Up Form."""
    name = StringField(
        'Name',
        validators=[InputRequired(message='Please enter name'),
                    Length(min=3, message='Name must be at least 3 symbols long')
        ]
    )
    email = EmailField(
        'Email',
        validators=[InputRequired(message='Please enter email address'),
                    Email(
                        message='Please enter valid email address',
                        check_deliverability=True
                    )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(message='Please enter password'),
                    Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*(&|%|#)).{8,}',
                           message='Password must contain at least one number, \
                                    one uppercase and lowercase letter, \
                                    one special symbol (&,$,#) and has at least \
                                    8 characters.'
                    )
        ]
    )
    password_confirm = PasswordField(
        'Password confirmation',
        validators=[InputRequired(message='Please enter your password again'),
                    EqualTo('password', message='Password confirmation does not match password')
        ]
    )
    recaptcha = RecaptchaField()

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """User Sign-In Form."""
    name = StringField(
        'Username',
        validators=[InputRequired(message='Please enter username')]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(message='Please enter password')]
    )
    remember_me = BooleanField(
        'Remember Me'
    )
    recaptcha = RecaptchaField()
    
    submit = SubmitField('Sign In')

class SimpleSearch(FlaskForm):
    """Search form for top-menu"""
    text = StringField(
        'Search',
        validators=[]
    )
    submit = SubmitField('Search')
