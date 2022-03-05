FROM python:3

RUN useradd photoric

WORKDIR /home/photoric

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

# patch Flask-Uploads to bring it in line with current Werkzeug version
#RUN   sed -i "s/from werkzeug import secure_filename, FileStorage|from werkzeug.utils import secure_filename\r\nfrom werkzeug.datastructures import  FileStorage\r\n/g" /venv/Lib/site-packages/flask_uploads.py

RUN venv/bin/pip install gunicorn

COPY photoric photoric
COPY migrations migrations
COPY .env ./
COPY boot.sh ./
RUN   sed -i "s/development|production/g" ./.env
RUN   sed -i "s/verytopsecretkeycode|$(echo date+%s | sha1sum)/g" ./.flaskenv
RUN   sed -i "s/verytopsecretkeycode|$(echo 'photoric'+date+%s | sha1sum)/g" ./.env
RUN chmod +x boot.sh

# ENV FLASK_APP wsgi.py

RUN chown -R photoric:photoric ./
USER photoric

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]