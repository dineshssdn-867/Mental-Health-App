from django.contrib import admin
from django.urls import path
from health.views import *

app_name = "health"
urlpatterns = [
    path('', Home.as_view(), name="home"),
]
