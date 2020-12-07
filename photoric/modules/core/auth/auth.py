"""Routes for user authentication"""
from flask import Blueprint, request, render_template
from ..helpers.forms.forms import LoginForm, SignupForm


# Blueprint initialization
auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    # SignIn logic


@auth.route('/signup', method=['GET', 'POST'])
def signup():
    """
    User Sign-Up

    GET requests should not reach this route
    POST requests validate form & user registration
    """
    form = SignupForm()
    if form.validate_on_submit():
        # TODO

    return render_template(
        'signup_form.html',
        title='New user sign-up',
        form=form
    )
    
