from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import datetime
import os

def get_profile_path(instance, filename):
    return os.path.join("profile", instance.username, filename)


class User(AbstractUser):
    CUSTOMER = 1
    DOCTOR = 2
    HOSPITAL = 3
    ROLES = (
        (CUSTOMER, "customer"),
        (DOCTOR, "doctor"),
        (HOSPITAL, "hospital"),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLES, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=True)

    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=get_profile_path, blank=True) # default
    address = models.CharField(max_length=255, null=True, blank=True)

    def is_email_verified(self):
        return self.email_verified


class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=settings.OTP_LENGTH, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.expires

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires = timezone.now() + datetime.timedelta(minutes=settings.OTP_EXPIRY)
        super(OTPModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} | {self.is_expired()}"
    

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    bloog_group = models.CharField(max_length=10, null=True, blank=True)
    disbled = models.BooleanField(default=False, blank=True)
    disease = models.CharField(null=True, blank=True, max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}"
    

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255)
    experties = models.CharField(max_length=200)
    experience = models.IntegerField()
    bio = models.TextField()
