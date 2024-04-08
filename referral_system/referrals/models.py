from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Referral(models.Model):
    referring_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    registration_timestamp = models.DateTimeField(auto_now_add=True)