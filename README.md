# code xample

## Learning new technologies by examples

Web application aggregating links to high quality code at GitHub, categorized by programming language and subjective difficulty of the code. It allows users to view, post, describe and 'like' such links. Final project for Distributed Web Applications course at University of Warsaw.

Flask application based on this comprehensive tutorial:
```
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
```
## Running the app

To run the application in dev mode: cd to cloned project directory, inside virtual env install required python packages (pip install -r requirements.txt) and enter in the terminal:
```
FLASK_APP=xample FLASK_ENV=development flask run
```

Alternatively build and run the docker container. Inside the cloned project directory:
```
docker build -t xample:latest .
docker run --name xample -d -p 5000:5000 --rm xample:latest
```

You can access the application at http://localhost:5000 .

## Users Microservice API ( http://localhost:5001 )

| Method  | Route | Arguments | Description |
| :---: | :---: | :---: | :---: |
| GET | / | - | API information |
| GET | /users | - | users information |
| GET | /user/id | - | user information |
| POST | /user | username, password | create new user |
| POST | /auth/login | username, password | verify login and password |

## Todo

* Split into microservices
* Add features: adding links, validating links, 'liking', asynchronously parsing information from the links destinations 
* Add minimalistic CSS
* Dockerize
