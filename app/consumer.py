from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection
from django.db.utils import OperationalError
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core import serializers
from django.utils import timezone
from django.utils.timezone import localtime
import json
from .models import *
from urllib.parse import urlparse
import datetime
import time
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from HarmoneyConnect import settings
import openai
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
#OPENAI_API_KEY = ''

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            await self.accept()
            self.room_group_name = self.scope['url_route']['kwargs']['room_name']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            openai.api_key = OPENAI_API_KEY
            prompt = (f"以下の文章に毒性のある言葉(暴言、不快な言葉など)が含まれる場合は、以下の出力:に続けて、毒性があるなら1を、そうでないなら0を出力してください。\
                      \n文章:'{message}'\
                      \n出力:")
            response = openai.Completion.create(
                model='text-davinci-003', 
                prompt=prompt,
                max_tokens=20,
            )
            if response['choices'][0]['text'] == '1':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message':'',
                        'toxic' : True,
                        'user_id':text_data_json['user_id'],
                        'created_time':None,
                    }
                )
            else:
                created_at=await self.createMessage(text_data_json)
                created_time=created_at.strftime('%H:%M')
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message':message,
                        'toxic' : False,
                        'user_id':text_data_json['user_id'],
                        'created_time':created_time
                    }
                )
        except Exception as e:
            print(e)

    async def chat_message(self, event):
        try:
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message,
                'toxic':event['toxic'],
                'user_id':event['user_id'],
                'created_time':event['created_time']
            }))
        except Exception as e:
            print(e)

    @database_sync_to_async
    def createMessage(self, event):
        try:
            room = Room.objects.get(
                id=self.room_group_name
            )
            user=CustomUser.objects.get(id=event['user_id'])
            _Message=Message.objects.create(
                room=room,
                user=user,
                content=event['message'],
                created_at=localtime(timezone.now())
            )
            entry=Entries.objects.get(user=user,room=room)
            entry.joined_at=_Message.created_at
            entry.save()
            return _Message.created_at
        except Exception as e:
            print(e)
    