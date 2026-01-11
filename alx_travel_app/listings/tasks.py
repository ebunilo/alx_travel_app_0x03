from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(to_email, booking_id, listing_title, guest_name, start_date, end_date, total_price):
    subject = f'Booking Confirmation for {listing_title}'
    message = f"""
    Dear {guest_name},

    Your booking has been confirmed!

    Booking Details:
    - Booking ID: {booking_id}
    - Listing: {listing_title}
    - Check-in: {start_date}
    - Check-out: {end_date}
    - Total Price: {total_price}

    Thank you for using ALX Travel App.

    Best regards,
    ALX Travel App Team
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )