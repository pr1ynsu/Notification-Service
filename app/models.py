from . import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # email, sms, in-app
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), default='sent')  # sent, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
