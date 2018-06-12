import json

import pika
import urllib.request


def validate_urls():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='urlValidationQueue')
    channel.basic_consume(validate_url,
                          queue='urlValidationQueue',
                          no_ack=True)
    channel.start_consuming()


def validate_url(ch, method, properties, body):
    message = json.loads(body)
    valid = True

    try:
        urllib.request.urlopen('https://github.com/' + message["url"])
    except urllib.error.HTTPError as e:
        if e.code != 200:
            valid = False

    request = urllib.request.Request('http://localhost:5002/post/' + str(message["id"]) + '/update',
                                     json.dumps({'link_accessible': valid}).encode('utf8'), method='POST',
                                     headers={'content-type': 'application/json'})

    urllib.request.urlopen(request)


if __name__ == '__main__':
    validate_urls()
