# ALX Travel App

A Django + Django REST Framework application for managing property listings, bookings, reviews, and payments via Chapa.

## Features

- Listings CRUD via REST API
- Booking creation with automatic price calculation
- Reviews with unique-per-user-per-listing constraint
- Payment initiation and verification with Chapa
- Swagger UI for API docs

## Tech Stack

- Django 5.2.9
- Django REST Framework
- drf-yasg (Swagger)
- django-environ
- django-cors-headers
- PostgreSQL
- Pillow (images)
- Celery + Redis (optional for email notifications)

## Test Result

### Initiate Payment via Postman

![Initiate Payment](images/initiate_payment.png)

### Make Payment via Chapa

![Chapa Payment UI](images/make_payment.png)

### Successful Payment UI

![Successful Payment UI](images/successful_payment.png)

### Verify Payment via Chapa

![Verify Payment](images/verify_payment.png)
