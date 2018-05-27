# code xample

## Learning new technologies by examples

Web application aggregating links to high quality code at GitHub, categorized by programming language and subjective difficulty of the code. It allows users to view, post, describe and 'like' such links. Final project for Distributed Web Applications course at University of Warsaw.

Flask application based on this comprehensive tutorial:
```
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
```
## Running the app

To run the application, install required python packages (listed in requirements.txt), cd to cloned project directory and enter in the terminal:
```
FLASK_APP=xample flask run
```

## Todo

* Add features: validating links, 'liking', asynchronously parsing information from the links destinations 
* Add minimalistic CSS
* Split into microservices
* Dockerize