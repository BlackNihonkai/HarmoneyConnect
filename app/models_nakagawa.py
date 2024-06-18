from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from HarmoneyConnect import settings
import uuid
from django.utils import timezone
from .models import *


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
# nakagawa
class Post(models.Model):
    title = models.CharField(max_length=400)
    content = models.TextField()
    image = models.ImageField(upload_to='', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    tag = models.ManyToManyField(Tag)

class Comment(models.Model):
    post = models.ForeignKey('app.Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
