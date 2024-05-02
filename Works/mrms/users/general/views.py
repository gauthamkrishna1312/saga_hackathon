from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views, get_user_model

from . import forms, base_views

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    user profile page
    """
    template_name = "general/user-profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            ""
        })


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
    def get_pattern_name(self):
        return reverse_lazy("users:profile", kwargs={"username": self.request.user.username})


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
    success_url = reverse_lazy("users:login")
