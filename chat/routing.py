from django.urls import path
from .consumers import ChatConsumer, StreamConsumer

websocket_urlpatterns = [
	path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
	path('ws/stream/<str:username>/', StreamConsumer.as_asgi()),
]