"""Routes for user authentication"""
from flask import Blueprint, request, render_template, redirect, abort
from flask_login import current_user, login_user, logout_user, LoginManager
from urllib.parse import urlparse, urljoin
from datetime import datetime

from .forms.forms import LoginForm, SignupForm
from .helper import get_user_by_name
from photoric.config.models import User


# Blueprint initialization
auth = Blueprint(
    'auth', __name__,
    url_prefix='/auth',
    template_folder='templates',
    static_folder='static'
)

# setup LoginManager object
login_manager = LoginManager()
login_manager.login_view = "auth.signin"


@before_after.before_app_first_request
def initial_setup():
    """ create admin user if not exist """
    if get_user_by_name('admin') is None:
        # create administrator role
        admin_role = Role(
            name='admin',
            restrictions= {}
        )
        # create administrators group
        admins_group = Group(
            name='admins',
            allowances='*'
        )
        # create private group
        private_group = Group(
            name='private',
            allowances=dict(
                gallery_items=['read'],
                albums=['read'],
                images=['read']
            )
        )
        # create contributors group
        contributors_group = Group(
            name='contributors',
            allowances=dict(
                gallery_items=['read', 'create', 'update', 'revoke'],
                albums=['read', 'create', 'update', 'revoke'],
                images=['read', 'create', 'update', 'revoke']
            )
        )
        # create user and map it to respective group annd role
        admin_user = User(name='admin', password=set_password('admin'))
        admin_user.roles = [admin_role]
        admin_user.groups = [admins_group, private_group, contributors_group]
        
        # insert new user, its role and group to to database
        db.session.add(
            admin_role, \
            admins_group, \
            private_group, \
            contributors_group, \
            admin_user
        )
        db.session.commit()


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    User Sign-In

    GET requests serve sign-in page
    POST requests validate form & log user in
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
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
        return redirect(next or url_for('views.index'))
    return render_template('auth/signin.html', title='Sign In', login_form=login_form)


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
            return redirect(url_for('views.index'))
        flash('A user already exists with that name.')

    return render_template(
        'auth/signup.html',
        title='New user registration',
        form=form
    )

@auth.route('/logout')
def logout():
    logout_user()
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
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.signin'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
