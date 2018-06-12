from http import HTTPStatus

import requests

# todo make part of the config
POSTS_URL = 'http://127.0.0.1:5002'


def get_all_technologies():
    response = requests.get(f'{POSTS_URL}/technologies')
    if response.status_code == HTTPStatus.OK:
        return response.json()
    else:
        raise Exception(response.content)


def get_all_difficulties():
    response = requests.get(f'{POSTS_URL}/difficulties')
    if response.status_code == HTTPStatus.OK:
        return response.json()
    else:
        raise Exception(response.content)


def get_post(post_id):
    response = requests.get(f'{POSTS_URL}/post/{post_id}')
    if response.status_code == HTTPStatus.OK:
        return response.json()
    else:
        raise Exception(response.content)


def get_filtered_posts(tech, diff):
    params = {'tech': tech, 'diff': diff}
    response = requests.get(f'{POSTS_URL}/posts', params=params)
    if response.status_code == HTTPStatus.OK:
        return response.json()
    else:
        raise Exception(response.content)


def create_post(author_name, title, body, link, technology, difficulty):
    if not all(var is not None for var in [author_name, title, body, link,
                                           technology, difficulty]):
        raise ValueError

    data = {
        'author_name': author_name,
        'title': title,
        'body': body,
        'link': link,
        'technology': technology,
        'difficulty': difficulty
    }
    response = requests.post(f'{POSTS_URL}/post', data=data)
    if response.status_code == HTTPStatus.CREATED.value:
        return response.json()
    else:
        raise Exception(response.content)
