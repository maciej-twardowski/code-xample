# code xample

## Learning new technologies by examples

Web application aggregating links to high quality code at GitHub, categorized by programming language and subjective difficulty of the code. It allows users to view, post and describe such links. Final project for Distributed Web Applications course at University of Warsaw.

Flask application based on this comprehensive tutorial:
```
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
```
## Screenshots

![alt text](https://i.imgur.com/FZxfeZj.png)
![alt text](https://i.imgur.com/wGvYfns.png)
![alt text](https://i.imgur.com/wPXwDx9.png)

## Running the app

To run the application using docker compose, cd to project root and type:
```
docker-compose up
```

You can access the application at http://0.0.0.0:5000 .

## Users Microservice API ( http://0.0.0.0:5001 )

| Method  | Route | Arguments | Description |
| :---: | :---: | :---: | :---: |
| GET | / | - | API information |
| GET | /users | - | users information |
| GET | /user/username | - | user information |
| POST | /user | username, password | create new user |
| POST | /user/username/verify | password | verify if password is valid |

## Posts Microservice API ( http://0.0.0.0:5002 )

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

## Authors

Marcin Brzeziński & Maciej Twardowski
