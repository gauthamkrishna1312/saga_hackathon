from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth import views as auth_views, get_user_model
from django.shortcuts import get_object_or_404, redirect

from . import forms, base_views
from users import models
from core.models import Hospital, DoctorHospitals, Appointment

class CustomerProfileView(generic.TemplateView):
    """
    user profile page
    """
    template_name = "general/user-profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        customer = get_object_or_404(models.Customer, user=self.request.user)
        appointment = Appointment.objects.filter(customer=customer)
        context.update({
            "patience": customer,
            "appointments": appointment,
        })
        return context

class DoctorProfileView(generic.TemplateView):
    """
    user profile page
    """
    template_name = "general/doctor_profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        doctor = get_object_or_404(models.Doctor, user__username=self.kwargs.get("username"))
        appointments = Appointment.objects.filter(doctor=doctor)
        hospitals = DoctorHospitals.objects.filter(doctor=doctor)
        context.update({
            "doctor": doctor,
            "appointments": appointments,
            "hospitals": hospitals
        })
        return context
    


class HospitalProfileView(generic.TemplateView):
    """
    user profile page
    """
    template_name = "general/hospital_profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        hospital = get_object_or_404(Hospital, user__username=self.kwargs.get("username"))
        doctors = DoctorHospitals.objects.filter(hospital=hospital)
        print(doctors)
        context.update({
            "hospital": hospital,
            "doctors": doctors,
            "no_of_doctors": doctors.count(),
        })
        return context



class LoginView(auth_views.LoginView):
    """
    Users Login View

    redirect user to url specified in settings.LOGIN_REDIRECT_URL
    set settings.LOGIN_REDIRECT_URL to 'users:redirect-logged-user'
    to redirect user based on the group or role
    """
    template_name = "general/user-login.html"
    form_class = forms.UserLoginForm
    redirect_authenticated_user = True
    pattern_name = "users:redirect-user"

    def get_redirect_url(self):
        return reverse_lazy(self.pattern_name)


class RedirectUserView(base_views.RedirectUserView):
    """
    Users Redirect View, redirect logged in user
    """
    def get_role_and_url(self):
        return {
            get_user_model().CUSTOMER: reverse_lazy("users:profile-customer", kwargs={"username": self.request.user.username}),
            get_user_model().DOCTOR: reverse_lazy("users:profile-doctor", kwargs={"username": self.request.user.username}),
            get_user_model().HOSPITAL: reverse_lazy("users:profile-hospital", kwargs={"username": self.request.user.username}),
        }
    

class CreateCustomerView(View):

    def get(self, request, *args, **kwargs):
        print(f"create customer {kwargs.get('id')}")
        user = get_object_or_404(get_user_model(), id=kwargs.get("id"))
        if not models.Customer.objects.filter(user=user).exists():
            print("Customer already exists")
            customer = models.Customer(user=user)
            customer.save()
        return redirect(reverse_lazy("users:login"))


class LogoutView(auth_views.LogoutView):
    """
    Users Logout View

    redirect user to login page
    """
    next_page = "users:login"
    http_method_names = ["GET", "get"]


class RegisterView(generic.CreateView):
    """
    User creation/registration view

    regular user is created and redirected to add the user in to a group
    """
    model = get_user_model()
    template_name = "general/user-register.html"
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy("users:add-customer-role")

    def get_success_url(self, *args, **kwargs):
        self.request.session["user_id"] = self.object.id
        return self.success_url


class AddCustomerRole(base_views.AddRole):
    """
    give users  the specified role
    """
    role = get_user_model().CUSTOMER
    success_url = reverse_lazy("users:add-to-customer-group")


class AddToCustomerGroup(base_views.AddToGroup):
    """
    add users to the specified group
    """
    group_name = "customer"

    def get_success_url(self):
        return reverse_lazy("users:create-customer", kwargs={"id": self.request.session.pop("user_id")})