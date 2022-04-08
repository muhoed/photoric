# photoric
python / flask based photo gallery

Photoric is a photography web-site constructor - SMS inspired by excellent Gallery Menalto project of the past and Google Photos look and DAM functionality. 
Photoric is written in Python using the micro framework Flask and a batch of Flask extension (see below). Bootstrap 4 and some genious JavaScripts and AJAX codes are in charge of the front-end styling and SQLite serves data stroing (will be replaced by PostgreSQL in production version).

The software is in development stage at the moment, no production release was issued yet. 

Currently, following features are implemented:

* backend:
    - automatic SQLite database creation and its initial setup required for first start
    - authorization and access rights management with ability to grant different access rights on user and group levels for almost all kind of content and web-site elements
    - dynamic navbars and its elements creation based on respective database entries including styling through classes and inline CSS

*frontend:
*site admin frontend:
    - album creation; album can contain unlimited number of subalbums
    - image upload to the main site and into albums including Drag'n'Drop functionality
    - albums / images selection for further operation with them
    - slide-show styled individual image view
    - basic settings / administration interface
* end-user frontend:
    - in progress

Core functionality to be added in the nearest future:

* backend:
    - improving of authorization functionality
    - restyling and extension of admin interface
    - full control over frontend styling through manual configuration and templating
    - no-script behavior
    - support of plugged in modules
    - deployment on NGINX and Apache
    - switch to PostgreSQL

* frontend
*site admin frontend:
    - albums functionality          - removing / deletion / sharing
    - images functionality          - show image info (including selected EXIF and IPTC data) / 
                                        zoom in/out (at individual view) / 
                                        add/move to album / 
                                        removing / deletion / sharing /
                                        download / basic edition
    - operations with selected 
    items                           - add to / remove from album /
                                        add to / remove from favorities collection /
                                        share / download as .zip / delete
*end-iser frontend:
    - end-user galleries, individual album and image views
    - commenting, sharing and collections/favorities functionality for registered users
    - contact form

A list of Flask extentions used by the moment (pls see requirements.txt for all dependances):
Flask-Admin
Flask-Authorize
Flask-Dropzone
Flask-JSGlue
Flask-Login
Flask-Session
Flask-SQLAlchemy
Flask-WTF
Flask-Uploads


Quickstart:

The software is in development stage, no production version exists yet. Source code can be downloaded here: https://github.com/muhoed/photoric/tree/dev.

To run application Python 3.6 >= is required and Python virtual environment is recommended. Config file provided assumes using Python dot environment for storing of base variables:

.flaskenv file content:
FLASK_APP="wsgi.py"
FLASK_ENV="development"

.env file content:
SECRET_KEY="your secret code"
PHOTO_STORAGE="name of folder in Flask instance folder to store database and uploaded images"
PROD_DATABASE="database name"

2020 @ Dmitry Argunov
GNU AFFERO GENERAL PUBLIC LICENSE





