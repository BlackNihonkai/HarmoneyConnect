from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,get_user_model,login,logout
from .models import *
from .models_nakagawa import *
from .models_nishio import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView

import os
import openai

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# create_post
def create_post(request):
    if request.method == 'POST':
        #title = request.POST['title']
        #content = request.POST['content']
        #post = Post.objects.create(title=title, content=content)
        form = PostForm(request.POST, request.FILES)# ハッシュタグ抽出開始
        if form.is_valid():
            post = form.save(commit=False)
            openai.api_key = OPENAI_API_KEY
            prompt = (f"以下の文章に毒性のある言葉(暴言、不快な言葉など)が含まれる場合は、以下の出力:に続けて、毒性があるなら1を、そうでないなら0を出力してください。\
                      \n文章:'{post.content}'\
                      \n出力:")
            response = openai.Completion.create(
                model='text-davinci-003', 
                prompt=prompt,
                max_tokens=20,
            )
            if response['choices'][0]['text'] == '1':
                return render(request, 'create_post.html', {'form':form,'user':request.user, 'toxic': "人が不快になる文章は避けましょう"})
            else:
                post.user = request.user
                post.save()
                form.save()
                words = form.cleaned_data["content"].split()
                for word in words:
                    if word[0] == "#":
                        if Tag.objects.filter(name=word[1:]).exists():
                            tag = Tag.objects.get(name=word[1:])
                        else:
                            tag = Tag.objects.create(name=word[1:])
                        post.tag.add(tag)
                #return redirect('post_list')
                return redirect('post_detail', post_id=post.id)
        #return redirect('post_detail', post_id=post.id)
        #return redirect('timeline')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'user':request.user})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts':posts})

#"""
def post_detail(request, post_id):
    post= Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})
#"""

# edit post
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user:
        return redirect('post_detail', post_id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form':form, 'post':post})

# delete post
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect(request, 'timeline')

# timeline
def timeline(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'timeline.html', {'posts':posts})

# home.html
def home(request):
    return render(request,'home.html')

# serch
#"""
#安定版
def search_posts_result(request):
    query = request.GET.get('q')    # 検索クエリを取得
    posts = Post.objects.filter(content__icontains=query).order_by('-created_at')   # コンテンツにクエリを含む投稿を検索
    #return render(request, 'search_post_results.html', {'posts':posts, 'query':query})
    return render(request, 'search.html', {'posts':posts, 'query':query})
#"""

def search(request):
    return render(request, 'search.html')

# search hashtags
#"""
## 安定版
def search_hashtags_result(request):
    form = TagSearchForm()
    posts = []
    if request.method == 'POST':
        form = TagSearchForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data['name']
            print("tag:{}".format(tag))
            posts = Post.objects.filter(tag__name__icontains=tag).order_by('-created_at')
    return render(request, 'search_hashtags_result.html', {'form':form, 'posts':posts})
    #return render(request, 'search.html', {'form':form, 'posts':posts})
#"""

def search_hashtags(request):
    return render(request, 'search_hashtags_result.html')

# add comment
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form':form, 'post':post})

# like 4 post
def like_timeline(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    #return redirect('post_detail', post_id=post_id)
    return redirect('timeline')

def like_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)