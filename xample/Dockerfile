FROM python:3.6-alpine

COPY . /xample
RUN pip install -r xample/requirements.txt
RUN pip install gunicorn

ENV FLASK_APP xample.py

EXPOSE 5000
CMD exec gunicorn -b :5000 --access-logfile - --error-logfile - xample:app