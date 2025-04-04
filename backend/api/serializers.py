from rest_framework import serializers
from .models import Contact, SocialMedia

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model
    """
    class Meta:
        model = Contact
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the SocialMedia model
    """
    class Meta:
        model = SocialMedia
        fields = '__all__'