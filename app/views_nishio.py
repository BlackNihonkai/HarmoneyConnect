from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,get_user_model,login,logout
from .models import *
from .models import CustomUser
from .models_nakagawa import *
from .models_nishio import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json

@login_required
def user_mypage(request):
    user = request.user # ログインユーザーを取得します
    # 必要な場合は、ユーザーに関連する他のデータを取得します

    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'user_mypage.html', {'user': user,'posts':posts})

"""
def user_search(request):
    form = UserSearchForm(request.GET)
    results = []

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        query = CustomUser.objects.all()

        if username:
            query = query.filter(username__icontains=username)

        if email:
            query = query.filter(email__icontains=email)

        results = query
    
    return render(request, 'user_search.html', {'form': form, 'results': results})
"""

class SearchUserView(LoginRequiredMixin,generic.ListView):
    model=CustomUser
    template_name='user_search.html'
    context_object_name = 'user_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        keyword_user=self.request.GET.get('keyword_user')
        if keyword_user:
            queryset=queryset.filter(username__icontains=keyword_user)
            return queryset[:10000]
        else:
            return CustomUser.objects.none()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        following_list=[]

        for searched_user in context['user_list']:
            followed_connections=searched_user.followed.all()
            followed = followed_connections.filter(following=self.request.user)
            if followed.exists():
                following_list.append(searched_user.id)

        context['following_list']=following_list
        
        return context

class profile_editView(LoginRequiredMixin,generic.UpdateView):
    model=get_user_model()
    form_class=CustomUserChangeForm
    template_name='profile_edit.html'
    success_url = reverse_lazy('user_mypage')

@login_required
def follow_func(request):
    if request.method =="POST":
        following = request.user
        follow_id=json.loads(request.body).get('follow_id')
        from_user_page=json.loads(request.body).get('from_user_page')
        followed_user = CustomUser.objects.get(pk=follow_id)
        connection = Connection.objects.filter(followed=followed_user,following=following)

        if connection.exists():
            connection.delete()
            followed=False
        else:
            connection.create(followed=followed_user, following=following)
            followed = True

        if from_user_page:
            follower_count=followed_user.followed.count()
            context={
            'follow_id': follow_id,
            'followed': followed,
            'follower_count': follower_count,
            }
        else:
            context={
                'follow_id': follow_id,
                'followed': followed,
            }
        
        if request.is_ajax():
            return JsonResponse(context)
        
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('timeline')