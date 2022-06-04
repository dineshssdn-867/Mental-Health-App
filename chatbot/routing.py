from django.urls import re_path
from .doctor import DoctorConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[^/]+)/', DoctorConsumer.as_asgi()),
]