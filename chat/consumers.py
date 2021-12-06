import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.group_id = "echo_1"

		async_to_sync(self.channel_layer.group_add)(
			self.group_id,
			self.channel_name
		)

		self.accept()


	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.group_id,
			self.channel_name
		)

	def receive(self, text_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		self.send(text_data=text_data)

	def echo_message(self, event):
		message = event['message']

		self.send(text_data=message)

class StreamConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user_id = self.scope['url_route']['kwargs']['username']
		self.group_name = f"chat_{self.user_id}"

		await self.channel_layer.group_add(
			self.group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.group_name,
			self.channel_name
		)

	async def receive(self, text_data=None, bytes_data=None):
		if text_data:
			text_data_json = json.loads(text_data)
			username = text_data_json['receiver']
			user_group_name = f"chat_{username}"

		await self.channel_layer.group_send(
			user_group_name,
			{
				'type': 'chat_message',
				'message': text_data
			}
		)

		await self.channel_layer.group_send(
			'echo_1',
			{
				'type': 'echo_message',
				'message': text_data
			}
		)



	async def chat_message(self, event):
		message = event['message']

		await self.send(text_data=message)