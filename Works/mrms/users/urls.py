from django.urls import path
from users import views
from users.general.urls import general_urlpatterns
from users.reset_password.urls import reset_urlpatterns
from users.change_password.urls import change_urlpatterns

urlpatterns = [
    *general_urlpatterns,
    *change_urlpatterns,
    *reset_urlpatterns,
]
