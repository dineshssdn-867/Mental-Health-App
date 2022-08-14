from django.contrib import admin
from django.urls import path
from .views import *

app_name = "AboutUs"
urlpatterns = [
    path('', AboutUs.as_view(), name="aboutus"),
]
