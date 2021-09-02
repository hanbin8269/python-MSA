import os, json, pika, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
from products.models import Product


params = pika.URLParameters(
    "amqps://uscxskut:u7NotCYJ5gcIWx3Abh3XYa5VLgKoLIbK@dingo.rmq.cloudamqp.com/uscxskut"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="admin")


def callback(ch, method, properties, body):
    print("Received in admin")
    data = json.loads(body)
    if properties.content_type == "product_like":
        product = Product.objects.get(id=data['id'])
        product.likes += 1
        product.save()
        print("product likes increased")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()
