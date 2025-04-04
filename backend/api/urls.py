from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, SocialMediaViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'social-media', SocialMediaViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]