from django.urls import path
from .views import *
from .views_nakagawa import *
from .views_nishio import *

urlpatterns = [
    #path('post/create/', create_post, name='create_post'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/', post_list, name='post_list'),
    #
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('home/',home,name='home'),
    path('timeline/', timeline, name='timeline'),
    path('search_posts_result/', search_posts_result, name='search_posts_result'),
    path('search_hashtags_result/', search_hashtags_result, name='search_hashtags_result'),
    path('search_hashtags/', search_hashtags, name='search_hashtags'),
    path('search/', search, name='search'),
    path('post/<int:post_id>/comment', add_comment, name='add_comment'),
    #path('like_for_post/', like_for_post, name='like_for_post'),
    path('post/<int:post_id>/like_timeline/', like_timeline, name='like_timeline'),
    path('post/<int:post_id>/like_detail/', like_detail, name='like_detail'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
]