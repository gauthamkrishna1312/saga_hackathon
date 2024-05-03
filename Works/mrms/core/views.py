from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import HospitalForm,DoctorForm, adddateForm
from . import models, mixins
from users.django_mail.views import SendEmailView, generate_uidb64_url


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "doctors": models.Doctor.objects.all(),
            "hospitals": models.Hospital.objects.all(),
        })
        return context
    

class AppointmentView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        doctor = get_object_or_404(models.Doctor, id=request.POST.get('doctor'))
        customer = get_object_or_404(models.Customer, user=request.user)
        appointment = models.Appointment(doctor=doctor, customer=customer)
        appointment.save()
        request.session["DOCTOR_EMAIL"] = doctor.user.email
        return redirect(reverse_lazy("core:appointment-confirm-mail"))
    


class AppointmentSendEmail(SendEmailView):
    email_subject = "Appointment Request"
    send_html_email = True
    email_template_name = "appointment-confirmation-mail.html"

    def get_from_email(self):
        return self.request.user.email
    
    def get_to_email(self):
        return self.request.session.pop("DOCTOR_EMAIL")
    
    def get_email_context_data(self):
        return {
            "patient": self.request.user,
        }
    
    def get_success_url(self):
        return reverse_lazy("users:profile-customer", kwargs={"username": self.request.user.username})


class AppointmentDecline(mixins.RoleRequiredMixin, View):
    role = get_user_model().DOCTOR

    def get(self, request, **kwargs):
        appointment = get_object_or_404(models.Appointment, id=kwargs.get("id"))
        appointment.status = models.Appointment.DECLINED
        appointment.save()
        self.request.session["APPO_ID"] = appointment.id
        return redirect(reverse_lazy("users:profile-doctor", kwargs={"username": self.request.user.username}))
    

class AppointmentAccept(mixins.RoleRequiredMixin, View):
    role = get_user_model().DOCTOR
    form_class = adddateForm

    def get_appointment_model(self):
        return get_object_or_404(models.Appointment, id=self.kwargs.get("id"))
    
    def render_to_response(self, context):
        return render(self.request, "confirm-appointment.html", context)
    
    def get_context_data(self, **kwargs):
        return {"appointment": self.get_appointment_model(), **kwargs}

    def get(self, request, **kwargs):
        return self.render_to_response(self.get_context_data(form=self.form_class))
    
    def form_valid(self, form):
        time = form.cleaned_data["time"]
        appointment = self.get_appointment_model()
        appointment.time = time
        appointment.save()
        self.request.session["PATIENT_EMAILID"] = appointment.customer.user.email
        self.request.session["APPO_ID"] = appointment.id
        return redirect(reverse_lazy("users:profile-doctor", kwargs={"username": self.request.user.username}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.form_valid(form)
        else:
            self.form_invalid(form)


class AppointmentAcceptmail(SendEmailView):
    email_subject = "Appointment Accepted"
    send_html_email = True
    email_template_name = "appointment-accept-mail.html"

    def get_from_email(self):
        return self.request.user.email
    
    def get_to_email(self):
        return self.request.session.pop("PATIENT_EMAILID")
    
    def get_email_context_data(self):
        return {
            "appointment": get_object_or_404(models.Appointment, id=self.request.session.pop("APPO_ID")),
            "status": "Accepted",
        }



class AppointmentDeclinemail(SendEmailView):
    email_subject = "Appointment Declined"
    send_html_email = True
    email_template_name = "appointment-decline-mail.html"

    def get_from_email(self):
        return self.request.user.email
    
    def get_to_email(self):
        return self.request.session.pop("PATIENT_EMAILID")
    
    def get_email_context_data(self):
        return {
            "appointment": get_object_or_404(models.Appointment, id=self.request.session.pop("APPO_ID")),
            "status": "Declined",
        }



class HospitalDetails(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
            form = HospitalForm()  # Assuming you have a HospitalForm defined
            return render(request, 'add_hospital_details.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = HospitalForm(request.POST)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.user = request.user
            hospital.save()
            return redirect('core:dashboard')  # Redirect to a dashboard or any other page after successful addition
        else:
            # If form is not valid, re-render the form with errors
            return render(request, 'add_hospital_details.html', {'form': form})


class DoctorDetails(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = DoctorForm()  # Assuming you have a HospitalForm defined
        return render(request, 'add_doctor_details.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user
            doctor.save()
            return redirect('core:dashboard')  # Redirect to a dashboard or any other page after successful addition
        else:
            # If form is not valid, re-render the form with errors
            return render(request, 'add_doctor_details.html', {'form': form})   
    

