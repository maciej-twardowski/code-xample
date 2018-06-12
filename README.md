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
(cd to users_microservice)
FLASK_APP=users FLASK_ENV=development flask run --port 5001
(cd to posts_microservice)
FLASK_APP=posts FLASK_ENV=development flask run --port 5002
python url_validator.py
(cd root project directory)
FLASK_APP=xample FLASK_ENV=development flask run
```

You can access the application at http://localhost:5000 .

## Users Microservice API ( http://localhost:5001 )

| Method  | Route | Arguments | Description |
| :---: | :---: | :---: | :---: |
| GET | / | - | API information |
| GET | /users | - | users information |
| GET | /user/username | - | user information |
| POST | /user | username, password | create new user |
| POST | /user/<username>/verify | password | verify if password is valid |

## Posts Microservice API ( http://localhost:5002 )

| Method  | Route | Arguments | Description |
| :---: | :---: | :---: | :---: |
| GET | / | - | API information |
| GET | /posts | technology, difficulty | posts information |
| GET | /post/id | - | post information |
| GET | /technologies | - | technologies information |
| GET | /technology/id | - | technology information |
| GET | /difficulties | - | difficulties information |
| GET | /difficulty/id | - | difficulty information |
| POST | /post | author_id, title, body, link, technology, difficulty | create new post |
| POST | /post/id/like | - | like existing post |
| POST | /post/id/update | link_accessible | set project accessibility

## Todo

* Split into microservices
* Posts microservice: Add list of users ids who liked the post to prevent from like abuse, think about better URL validation
* Add features: adding links, validating links, 'liking', asynchronously parsing information from the links destinations 
* Add minimalistic CSS
* Dockerize
