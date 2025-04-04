from rest_framework import viewsets
from .models import Contact, SocialMedia
from .serializers import ContactSerializer, SocialMediaSerializer

class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for contacts
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class SocialMediaViewSet(viewsets.ModelViewSet):
    """
    API endpoint for social media
    """
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
