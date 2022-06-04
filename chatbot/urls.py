from django.urls import path  # Importing necessary libraries for urls
from .views import *  # Importing all the views from views.py

app_name = 'chatbot'  # Initializing app name
urlpatterns = [
    path('bot/', chatPage, name="bot"),
    path('chat/<str:room_name>/', room, name='room'),
]
