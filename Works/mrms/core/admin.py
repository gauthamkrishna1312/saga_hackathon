from django.contrib import admin
from . import models


admin.site.register(models.Hospital)
admin.site.register(models.ImageHospital)
admin.site.register(models.DoctorHospitals)
admin.site.register(models.Appointment)