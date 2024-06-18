from django.urls import path
from .views import *
from .views_nakagawa import *
from .views_nishio import *

urlpatterns = [
    # トップ画面
    
    path('user_search/',SearchUserView.as_view() , name='user_search'),
    path('user_mypage/', user_mypage, name='user_mypage'),
    path('profile-edit/<int:pk>',profile_editView.as_view(),name='profile_edit'),
    path('follow/',follow_func, name='follow'),
    path('delete_post/<int:post_id>', delete_post, name='delete_post'),
]