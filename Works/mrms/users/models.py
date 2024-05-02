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
    HOPITAL = 3
    ROLES = (
        (CUSTOMER, "customer"),
        (DOCTOR, "doctor"),
        (HOPITAL, "hospital"),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLES, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=True)

    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=get_profile_path)

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
