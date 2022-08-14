from django.urls import path  # Importing necessary libraries for urls
from .views import *  # Importing all the views from views.py

app_name = 'predictor'  # Initializing app name
urlpatterns = [
    path('show_emotion/', FormViewEmotion.as_view(), name="show_emotion"),  # Connecting the url route to the view with namespace of show_emotion
    path('show_emotion_result/', show_emotion, name="show_emotion_result"),  # Connecting the url route to the view with namespace of show_emotion_result
]
