from flask import Blueprint, request, jsonify
from .models import Notification
from . import db
import pika
import json

main = Blueprint('main', __name__)

@main.route('/notifications', methods=['POST'])
def send_notification():
    data = request.get_json()
    notification = Notification(
        user_id=data['user_id'],
        type=data['type'],
        message=data['message'],
        status='pending'  # start as pending
    )
    db.session.add(notification)
    db.session.commit()

    # Connect to RabbitMQ and publish the notification ID for processing
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='notifications_queue',
        body=json.dumps({'notification_id': notification.id}),
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )
    connection.close()

    return jsonify({"message": "Notification queued for sending"}), 202

@main.route('/users/<int:user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    result = []
    for n in notifications:
        result.append({
            'id': n.id,
            'type': n.type,
            'message': n.message,
            'status': n.status,
            'created_at': n.created_at.isoformat()
        })
    return jsonify(result)
