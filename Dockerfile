FROM python:3.6-alpine

RUN adduser -D xample

WORKDIR /home/code-xample

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY xample xample
COPY migrations migrations
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R xample:xample ./
USER xample

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]