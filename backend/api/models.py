from django.db import models

class Contact(models.Model):
    """
    Model for storing contact information
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    """
    Model for storing social media information
    """
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50)  # Font Awesome icon class
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
