import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .response import get_bot_response


class DoctorConsumer(WebsocketConsumer):
    asked_question = " "

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.asked_question = text_data_json['message']
        msg = 'not found'
        ans = get_bot_response(self.asked_question)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(

            self.room_group_name,
            {
                'type': 'chat_message',
                'answer': ans,
                'q': self.asked_question
            }

        )

    # Receive message from room group
    def chat_message(self, event):
        ans = event['answer']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'answer': ans,
            'q': self.asked_question
        }))
