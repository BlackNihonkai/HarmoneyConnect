from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from HarmoneyConnect import settings
import uuid
from django.utils import timezone
from .models import *
from .models import CustomUser
from django import forms

class UserSearchForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

class Connection(models.Model):
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE,null=True)
    followed = models.ForeignKey(CustomUser, related_name='followed', on_delete=models.CASCADE,null=True)