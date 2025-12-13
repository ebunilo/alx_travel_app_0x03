from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
# Swagger/OpenAPI
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel App API",
        default_version='v1',
        description="API for listings and bookings",
        # contact=openapi.Contact(email=""),
        # license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Mount RESTful endpoints under /api/
    path('api/', include(router.urls)),
    # Swagger UI and raw schema
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc'),
    path('api/schema.json', schema_view.without_ui(cache_timeout=0), name='api-schema-json'),
    path('api/schema.yaml', schema_view.without_ui(cache_timeout=0), name='api-schema-yaml'),
]
