"""Routes for user authentication"""
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse, urljoin
from datetime import datetime

from photoric.modules.auth.forms import LoginForm, SignupForm
# from photoric.modules.auth.helper import create_user, get_user_by_name
from photoric import db
from photoric.modules.auth.models import User
from photoric.modules.auth import auth_bp, login_manager, authorize


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    User Sign-In

    GET requests serve sign-in page
    POST requests validate form & log user in
    """

    # redirect user to home page if it is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))

    # check provided credentials and log user in
    login_form = LoginForm()
    if login_form.validate_on_submit():
        #user = get_user_by_name(name=login_form.name.data)
        user = User.get_by_name(name=login_form.name.data)
        if user is None or not user.check_password(login_form.password.data):
            flash(u'Invalid username or password', 'danger')
            return redirect(url_for('auth.signin'))
        login_user(user, remember=login_form.remember_me.data)

        # remember login date and time
        user.last_login = "set"

        # return logged in user to the requested page or home page if not
        return_page = request.args.get('next')
        flash(u'You were successfully logged in as ' + current_user.name, 'success')
        if not is_safe_url(return_page):
            return redirect(url_for('views.index'))
        return redirect(return_page or url_for('views.index'))

    # load log in dialog if GET method
    return render_template('auth/signin.html', title='Sign In', form=login_form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User Sign-Up

    GET requests serve sign-up page
    POST requests validate form & user registration
    """
    form = SignupForm()
    if form.validate_on_submit():
        # prepare new user data
        data = {}
        data["name"] = form.name.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        # create new user
        # new_user =  User(
        #    name = form.name.data,
        #    email = form.email.data,
        #    password = form.password.data
        #)
        
        user = User.create_from_json(data)
        
        login_user(user)  # Log in as newly created user
        
        # remember login date and time
        user.last_login = "set"

        flash(u'Congratulation! You were successfully registered!', 'success')
        return redirect(url_for('views.index'))

    return render_template(
        'auth/signup.html',
        title='New user registration',
        form=form
    )


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash(u'You were logged out', 'info')
    return redirect(url_for('views.index'))

    
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash(u'You must be logged in to view that page.', 'warning')
    return redirect(url_for('auth.signin'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
