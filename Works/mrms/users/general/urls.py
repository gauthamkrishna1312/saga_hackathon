from django.urls import path
from . import views

general_urlpatterns = [
    # redirect user based on authentication and authorisation
    path('', views.RedirectUserView.as_view(), name="redirect-user"),
    # profile page
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

    # user login
    path('login/', views.LoginView.as_view(), name='login'),
    # user logout
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # user registration
    path('register/', views.RegisterView.as_view(), name='signup'),
    # add a role to the registered user
    path('register/add-role', views.AddCustomerRole.as_view(), name='add-customer-role'),
    # add the registered user to a group
    path('register/add-group/', views.AddToCustomerGroup.as_view(), name='add-to-customer-group'),
]