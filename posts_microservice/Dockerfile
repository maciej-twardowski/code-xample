FROM python:3.6-alpine

COPY . /posts_microservice
WORKDIR  /posts_microservice
RUN pip install -r requirements.txt

ENV FLASK_APP posts
EXPOSE 5001
CMD flask run --host 0.0.0.0 --port 5001
