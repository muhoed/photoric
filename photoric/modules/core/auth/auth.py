"""Routes for user authentication"""
from flask import Blueprint, request, render_template, redirect, abort
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse, urljoin
from datetime import datetime

from photoric.config.models import login_manager
from photoric.modules.core.helpers.forms.forms import LoginForm, SignupForm
from photoric.modules.core.helpers.database.db import get_user_by_name
from photoric.config.models import User


# Blueprint initialization
auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    User Sign-In

    GET requests serve sign-in page
    POST requests validate form & log user in
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('itemviews.index'))
    login_form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_name(name=form.name.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.signin'))
        login_user(user, remember=form.remember_me.data)
        current_user.last_login = datetime.now
        next = request.args.get('next')
        if not is_safe_url(next):
        	return abort(400)
        return redirect(next or url_for('itemviews.index'))
    return render_template('signin.html', title='Sign In', login_form=login_form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User Sign-Up

    GET requests serve sign-up page
    POST requests validate form & user registration
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = get_user(name=form.name.data)
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.hash_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            flash('Congratulation! You were successfully registered!')
            return redirect(url_for('itemviews.index'))
        flash('A user already exists with that name.')

    return render_template(
        'signup_form.html',
        title='New user registration',
        form=form
    )

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('itemviews.index'))

    
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.signin'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
