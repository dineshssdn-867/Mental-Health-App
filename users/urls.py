from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path('login', UserLoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('logout', UserLogoutView.as_view(), name="logout"),
]
