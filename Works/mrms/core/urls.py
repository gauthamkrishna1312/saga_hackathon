from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('appoint/', views.AppointmentView.as_view(), name="appointment"),
    path('appoint/confirm/mail/', views.AppointmentSendEmail.as_view(), name="appointment-confirm-mail"),
    path('appoint/confirm/', views.AppointmentAccept.as_view(), name="appointment-confirm"),
    path('appoint/declined/', views.AppointmentDecline.as_view(), name="appointment-declined"),
    path('appoint/status/mail/', views.AppointmentAcceptmail.as_view(), name="appointment-accept-mail"),
    path('appoint/status/mail/', views.AppointmentAcceptmail.as_view(), name="appointment-accept-mail"),
    path('doctor/create/', views.DoctorDetails.as_view(), name="doctor-add"),
    path('hospital/create/', views.HospitalDetails.as_view(), name="hospital-add"),
]