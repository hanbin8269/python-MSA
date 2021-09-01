import pika, json

params = pika.URLParameters(
    "amqps://uscxskut:u7NotCYJ5gcIWx3Abh3XYa5VLgKoLIbK@dingo.rmq.cloudamqp.com/uscxskut"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="main", body=json.dumps(body), properties=properties
    )
