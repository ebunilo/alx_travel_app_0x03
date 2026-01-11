# ALX Travel App

A Django + Django REST Framework application for managing property listings, bookings, reviews, and payments via Chapa, with background email notifications.

## Features

- Listings CRUD via REST API
- Booking creation with automatic price calculation
- Reviews with unique-per-user-per-listing constraint
- Payment initiation and verification with Chapa
- Email notifications for booking confirmations via Celery and RabbitMQ
- Swagger UI for API docs

## Tech Stack

- Django 5.2.9
- Django REST Framework
- drf-yasg (Swagger)
- django-environ
- django-cors-headers
- PostgreSQL
- Pillow (images)
- Celery + RabbitMQ (for background tasks and email notifications)
- Redis (for caching, optional)

## Setup

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure your environment variables (database, email, Chapa secret, etc.).
6. Run migrations: `python manage.py migrate`
7. Start RabbitMQ (via Docker: `docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3-management-alpine`)
8. Start the Celery worker: `celery -A alx_travel_app worker --loglevel=info`
9. Run the Django server: `python manage.py runserver`

For Docker setup, use `docker-compose up -d` to start all services including RabbitMQ and Celery.

## Test Result

### Initiate Payment via Postman

![Initiate Payment](images/initiate_payment.png)

### Make Payment via Chapa

![Chapa Payment UI](images/make_payment.png)

### Successful Payment UI

![Successful Payment UI](images/successful_payment.png)

### Verify Payment via Chapa

![Verify Payment](images/verify_payment.png)
