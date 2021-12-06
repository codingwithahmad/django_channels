from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe
import json

# Create your views here.
def index(request):
	return HttpResponse('Hello')

def room(request, room_name):
	return render(request, 'chat/chat_room.html', {
		'room_name': room_name
	})

def stream(request, username):
	return render(request, 'chat/chat.html', {'username_json': mark_safe(json.dumps(username))})