from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.views import *
from app.consumer import *
from django.core.asgi import get_asgi_application
import django
import os

websocket_urlpatterns = [
    path('<str:room_name>', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    "http": get_asgi_application(),
})

