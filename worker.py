import pika
import json
import time
from app import create_app, db
from app.models import Notification
from retry import retry

app = create_app()
app.app_context().push()  # Needed to access Flask app context and DB

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='notifications_queue', durable=True)

@retry(tries=3, delay=2)
def process_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        print(f"[Worker] Notification {notification_id} not found in DB")
        return

    try:
        if notification.type == 'email':
            print(f"[Worker] Sending EMAIL to user {notification.user_id}: {notification.message}")
        elif notification.type == 'sms':
            print(f"[Worker] Sending SMS to user {notification.user_id}: {notification.message}")
        elif notification.type == 'in-app':
            print(f"[Worker] Creating in-app notification for user {notification.user_id}: {notification.message}")
        else:
            raise ValueError(f"Unknown notification type: {notification.type}")

        time.sleep(1)  # simulate sending delay

        notification.status = 'sent'
        db.session.commit()
        print(f"[Worker] Notification {notification_id} marked as sent")

    except Exception as e:
        print(f"[Worker] Error sending notification {notification_id}: {e}")
        notification.status = 'failed'
        db.session.commit()
        raise  # This triggers the retry decorator

def callback(ch, method, properties, body):
    data = json.loads(body)
    notification_id = data.get('notification_id')
    print(f"[Worker] Received notification {notification_id} for processing")

    try:
        process_notification(notification_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Ack only if processed successfully
    except Exception as e:
        print(f"[Worker] Failed to process notification {notification_id}: {e}")
        # Message will NOT be acked, so RabbitMQ will retry

channel.basic_qos(prefetch_count=1)  # Fair dispatch
channel.basic_consume(queue='notifications_queue', on_message_callback=callback)

print("[Worker] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
