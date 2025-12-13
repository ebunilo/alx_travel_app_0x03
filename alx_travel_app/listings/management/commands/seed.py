import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking

TITLES = [
    "Cozy Downtown Apartment",
    "Spacious Family House",
    "Modern Beachfront Condo",
    "Luxury Hilltop Villa",
    "Quiet Suburban Retreat",
    "City Center Studio",
    "Rustic Mountain Cabin",
    "Elegant Penthouse Suite",
]

DESCRIPTIONS = [
    "A lovely place close to amenities.",
    "Perfect for families and long stays.",
    "Stunning views and modern design.",
    "Premium finishes with private pool.",
    "Comfortable and peaceful area.",
]

LOCATIONS = [
    "New York, USA",
    "San Francisco, USA",
    "Paris, France",
    "Berlin, Germany",
    "Nairobi, Kenya",
    "Cape Town, South Africa",
    "Tokyo, Japan",
]

PROPERTY_TYPES = ['apartment', 'house', 'villa', 'condo']


class Command(BaseCommand):
    help = "Seed the database with sample listings and bookings"

    def handle(self, *args, **options):
        host, _ = User.objects.get_or_create(
            username='demo_host',
            defaults={'email': 'host@example.com', 'password': 'demo12345'}
        )

        guest, _ = User.objects.get_or_create(
            username='demo_guest',
            defaults={'email': 'guest@example.com', 'password': 'demo12345'}
        )

        created_count = 0
        for title in TITLES:
            if Listing.objects.filter(title=title).exists():
                continue
            listing = Listing.objects.create(
                title=title,
                description=random.choice(DESCRIPTIONS),
                price=random.randint(50, 500),
                property_type=random.choice(PROPERTY_TYPES),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                location=random.choice(LOCATIONS),
                host=host,
            )
            created_count += 1

            # Create a sample booking
            start = date.today() + timedelta(days=random.randint(1, 30))
            end = start + timedelta(days=random.randint(2, 7))
            Booking.objects.create(
                listing=listing,
                guest=guest,
                start_date=start,
                end_date=end,
                guests=random.randint(1, 4),
            )

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Listings created: {created_count}"))