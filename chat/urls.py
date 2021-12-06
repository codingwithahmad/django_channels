from django.urls import path
from .views import index, room, stream


urlpatterns = [
	path('', index, name='index'),
	path('chat/<str:room_name>/', room, name='room'),
	path('stream/<str:username>/', stream, name='stream')
]