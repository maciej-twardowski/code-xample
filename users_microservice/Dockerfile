FROM python:3.6-alpine

COPY . /users_microservice
WORKDIR  /users_microservice
RUN pip install -r requirements.txt

ENV FLASK_APP users
EXPOSE 5001
CMD flask run --host 0.0.0.0 --port 5001
