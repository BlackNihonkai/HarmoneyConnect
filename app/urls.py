from django.urls import path
from .views import *
from .views_nakagawa import *
from .views_nishio import *

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    path('',SignupView.as_view(),name='signup'),
    path('login/',login_func,name='login'),
    path('logout/',logout_func,name='logout'),
    path('chat/<int:user_id>', Chat.as_view(), name='Chat'),
    path('chat-room/<uuid:room_id>', chat_room, name='chat_room'),
    path('room/<int:pk>', room, name='room'),
    path('cat-video/', search_cat_video_on_youtube, name='CatVideo'),
    path('user-page/<int:pk>/',UserPageView.as_view(), name='UserPage'),
]
