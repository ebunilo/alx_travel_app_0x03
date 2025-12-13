from rest_framework import serializers
from .models import Listing, ListingImage, Booking

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'caption', 'is_primary']

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    host_name = serializers.CharField(source='host.get_full_name', read_only=True)
    average_rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'property_type',
            'bedrooms', 'bathrooms', 'location', 'latitude', 'longitude',
            'is_available', 'created_at', 'updated_at', 'host', 'host_name',
            'average_rating', 'images'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'host_name', 'average_rating']

class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    guest_username = serializers.CharField(source='guest.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest', 'guest_username',
            'start_date', 'end_date', 'guests', 'total_price', 'status',
            'created_at'
        ]
        read_only_fields = ['id', 'total_price', 'status', 'created_at']