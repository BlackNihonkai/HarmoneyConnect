from django import forms
import re
from django.contrib.auth import get_user_model
from .models_nakagawa import *


def isalnum(password):
    password_reg=re.compile('\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,100}\Z')
    return password_reg.match(password) is not None

class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード(再入力)'}))

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder': 'メールアドレス'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder': 'ユーザー名'})

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if isalnum(password1):
            return password1
        else:
            raise forms.ValidationError('※半角英小文字大文字数字をそれぞれ1種類以上含む8文字以上100文字以下の\nパスワードを設定して下さい')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('※1回目とパスワードが異なります')
        else:
            return password2

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user   


    class Meta:
        model = get_user_model()
        fields = ('email','username')

class CustomUserChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            super(CustomUserChangeForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class' : 'form-control'})
            self.fields['profile'].widget.attrs.update({'class' : 'form-control'})

    ProfileImage = forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = get_user_model()
        fields = ('username','ProfileImage','profile')

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)

    image = forms.ImageField(widget=forms.widgets.FileInput, required=False)

    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class TagSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'ハッシュタグ検索'}))