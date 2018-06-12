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
    print(f'Got new URL to check: {message["url"]}.')

    try:
        urllib.request.urlopen('https://github.com/' + message["url"])
    except urllib.error.HTTPError as e:
        if e.code != 200:
            valid = False

    print(f'Checking done. Link accessible: {valid}.')
    request = urllib.request.Request('http://localhost:5002/post/' + str(message["id"]) + '/update',
                                     json.dumps({'link_accessible': valid}).encode('utf8'), method='POST',
                                     headers={'content-type': 'application/json'})

    urllib.request.urlopen(request)
    print(f'Post status updated.')


if __name__ == '__main__':
    print("Validator worker started. Waiting for tasks to do...")
    validate_urls()
