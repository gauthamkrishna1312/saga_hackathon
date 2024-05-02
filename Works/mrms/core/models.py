from django.db import models
from django.contrib.auth import get_user_model
from users.models import Doctor, Customer
import os


class Hospital(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    beds = models.IntegerField() # wards
    rooms = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username}"


def Image_path(instance, filename):
    return os.path.join("hospitals", instance.hospital.user.username, filename)


class ImageHospital(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Image_path)

    def __str__(self):
        return f"{self.hospital.user.username}"



class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"



class HospitalLab(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hospital.user.username}"



class DoctorHospitals(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor.user.username} | {self.hospital.user.username}"



class Appointment(models.Model):
    # default status pending
    ACCEPTED = 2
    DECLINED = 1
    PENDING = 0
    STATUS_CHOICES = (
        (ACCEPTED, "appointed"),
        (DECLINED, "declined")
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.customer.user.username} | {self.doctor.user.username}"

