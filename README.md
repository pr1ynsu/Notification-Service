````markdown
# Notification Service

A Flask-based notification service with RabbitMQ worker for asynchronous notification processing.

## Features

- REST API to create notifications (`email`, `sms`, `in-app`).
- Notifications saved in a database with status tracking.
- RabbitMQ queue for async processing.
- Worker process that consumes notifications, simulates sending, and updates status.
- Simple retry logic on failures.

## Tech Stack

- Python 3.x
- Flask
- Flask-SQLAlchemy
- RabbitMQ (pika client)
- SQLite (or your choice of database)
- retry package for retry logic

## Setup & Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/notification-service.git
cd notification-service
````

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Make sure RabbitMQ is installed and running locally:

* [RabbitMQ installation guide](https://www.rabbitmq.com/download.html)

5. Run database migrations or create the database (if applicable):

```bash
python
>>> from app import db, create_app
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

6. Start the Flask app:

```bash
python run.py
```

7. In a new terminal, start the worker:

```bash
python worker.py
```

## API Endpoints

* **POST /notifications**

  Create a new notification.
  Request body (JSON):

  ```json
  {
    "user_id": 1,
    "type": "email",
    "message": "Welcome!"
  }
  ```

* **GET /users/\<user\_id>/notifications**

  Get all notifications for a specific user.

## Testing with curl

Send notification:

```bash
curl -X POST http://127.0.0.1:5000/notifications -H "Content-Type: application/json" -d "{\"user_id\":1,\"type\":\"email\",\"message\":\"Hello!\"}"
```

Get user notifications:

```bash
curl http://127.0.0.1:5000/users/1/notifications
```
