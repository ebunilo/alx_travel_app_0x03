from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.conf import settings
import requests
import uuid

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email

# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]  # adjust as needed

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]  # adjust as needed

    def create(self, request, *args, **kwargs):
        # Create the booking first
        response = super().create(request, *args, **kwargs)
        if response.status_code not in (drf_status.HTTP_201_CREATED,):
            return response

        booking = Booking.objects.get(pk=response.data['id'])
        # Trigger email task asynchronously
        send_booking_confirmation_email.delay(
            to_email=booking.guest.email,
            booking_id=booking.id,
            listing_title=booking.listing.title,
            guest_name=booking.guest.get_full_name() or booking.guest.username,
            start_date=booking.start_date,
            end_date=booking.end_date,
            total_price=str(booking.total_price),
        )

        booking_id = response.data.get("id")
        # Derive payment fields
        amount = response.data.get("total_price")
        currency = request.data.get("currency", "ETB")
        # Pull email/name from request or related user
        email = request.data.get("email") or (self.get_queryset().model.guest.field.remote_field.model.objects.get(pk=response.data["guest"]).email if response.data.get("guest") else None)
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        phone_number = request.data.get("phone_number", "")

        if not all([booking_id, amount, email]):
            # If we cannot initiate payment, just return booking with warning
            response.data["payment_initiation"] = {"status": "failed", "detail": "Missing data to initiate payment (booking_id/amount/email)."}
            return response

        # Initialize Chapa payment
        tx_ref = f"booking-{booking_id}-{uuid.uuid4().hex[:8]}"
        payload = {
            "amount": str(amount),
            "currency": currency,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "tx_ref": tx_ref,
            "return_url": request.data.get("return_url", ""),
            "callback_url": request.data.get("callback_url", ""),
            "customization": {
                "title": "Payment",
                "description": f"Payment for booking id {booking_id}",
            },
        }
        headers = {
            "Authorization": f"Bearer {getattr(settings, 'CHAPA_SECRET_KEY', '')}",
            "Content-Type": "application/json",
        }
        if not headers["Authorization"].strip():
            response.data["payment_initiation"] = {"status": "failed", "detail": "Chapa secret key not configured."}
            return response

        try:
            chapa_resp = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers, timeout=20)
            data = chapa_resp.json() if chapa_resp.headers.get("Content-Type", "").startswith("application/json") else {"status": "failed"}
        except requests.RequestException as e:
            response.data["payment_initiation"] = {"status": "failed", "detail": f"Payment initialization failed: {e}"}
            return response

        if data.get("status") != "success":
            response.data["payment_initiation"] = {"status": "failed", "detail": data.get("message", "Failed to initialize payment"), "data": data.get("data")}
            return response

        checkout_url = data.get("data", {}).get("checkout_url")
        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            response.data["payment_initiation"] = {"status": "failed", "detail": "Booking not found after creation."}
            return response

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            currency=currency,
            status=Payment.STATUS_PENDING,
            tx_ref=tx_ref,
            checkout_url=checkout_url,
            chapa_transaction_id=data.get("data", {}).get("id")
        )

        response.data["payment_initiation"] = {
            "status": "success",
            "checkout_url": checkout_url,
            "tx_ref": payment.tx_ref,
            "payment_id": payment.id,
        }
        return response

class InitiatePaymentView(APIView):
    permission_classes = [permissions.AllowAny]  # adjust as needed

    def post(self, request):
        booking_id = request.data.get("booking_id")
        amount = request.data.get("amount")
        currency = request.data.get("currency", "ETB")
        email = request.data.get("email")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        phone_number = request.data.get("phone_number", "")

        if not all([booking_id, amount, email]):
            return Response({"detail": "booking_id, amount, and email are required."}, status=drf_status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=drf_status.HTTP_404_NOT_FOUND)

        tx_ref = f"booking-{booking_id}-{uuid.uuid4().hex[:8]}"

        payload = {
            "amount": str(amount),
            "currency": currency,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "tx_ref": tx_ref,
            "return_url": request.data.get("return_url", ""),
            "callback_url": request.data.get("callback_url", ""),
            "customization": {
                "title": "Payment",
                "description": f"Payment for booking id {booking_id}",
            },
        }
        headers = {
            "Authorization": f"Bearer {getattr(settings, 'CHAPA_SECRET_KEY', '')}",
            "Content-Type": "application/json",
        }

        if not headers["Authorization"].strip():
            return Response({"detail": "Chapa secret key not configured."}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            chapa_resp = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers, timeout=20)
        except requests.RequestException as e:
            return Response({"detail": f"Payment initialization failed: {e}"}, status=drf_status.HTTP_502_BAD_GATEWAY)

        data = chapa_resp.json() if chapa_resp.headers.get("Content-Type", "").startswith("application/json") else {"status": "failed"}
        if data.get("status") != "success":
            return Response({"detail": data.get("message", "Failed to initialize payment"), "data": data.get("data")}, status=drf_status.HTTP_400_BAD_REQUEST)

        checkout_url = data.get("data", {}).get("checkout_url")
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            currency=currency,
            status=Payment.STATUS_PENDING,
            tx_ref=tx_ref,
            checkout_url=checkout_url,
            chapa_transaction_id=data.get("data", {}).get("id")  # if Chapa returns an id; may be None
        )

        return Response(
            {
                "message": "Hosted Link",
                "status": "success",
                "data": {
                    "checkout_url": checkout_url,
                    "tx_ref": payment.tx_ref,
                    "payment_id": payment.id,
                },
            },
            status=drf_status.HTTP_200_OK,
        )

class VerifyPaymentView(APIView):
    permission_classes = [permissions.AllowAny]  # adjust as needed

    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")
        if not tx_ref:
            return Response({"detail": "tx_ref is required."}, status=drf_status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=drf_status.HTTP_404_NOT_FOUND)

        headers = {
            "Authorization": f"Bearer {getattr(settings, 'CHAPA_SECRET_KEY', '')}",
            "Content-Type": "application/json",
        }
        if not headers["Authorization"].strip():
            return Response({"detail": "Chapa secret key not configured."}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Chapa verification typically uses /v1/transaction/verify/{tx_ref}
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        try:
            chapa_resp = requests.get(url, headers=headers, timeout=20)
        except requests.RequestException as e:
            return Response({"detail": f"Verification failed: {e}"}, status=drf_status.HTTP_502_BAD_GATEWAY)

        data = chapa_resp.json() if chapa_resp.headers.get("Content-Type", "").startswith("application/json") else {"status": "failed"}
        chapa_status = data.get("status")

        if chapa_status == "success":
            payment.status = Payment.STATUS_COMPLETED
            payment.save(update_fields=["status", "updated_at"])
            # Send confirmation email via Celery if available
            if send_payment_confirmation_email:
                try:
                    send_payment_confirmation_email.delay(
                        to_email=payment.booking.guest.email,
                        booking_id=payment.booking_id,
                        amount=str(payment.amount),
                        tx_ref=payment.tx_ref,
                    )
                except Exception:
                    # Gracefully ignore email errors
                    pass
        else:
            payment.status = Payment.STATUS_FAILED
            payment.save(update_fields=["status", "updated_at"])

        return Response(
            {
                "status": "success" if chapa_status == "success" else "failed",
                "payment_status": payment.status,
                "data": data.get("data"),
            },
            status=drf_status.HTTP_200_OK if chapa_status == "success" else drf_status.HTTP_400_BAD_REQUEST,
        )
