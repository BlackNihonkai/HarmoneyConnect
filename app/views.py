from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,get_user_model,login,logout
from .models import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from . import youtube


class SignupView(generic.CreateView):
    model=get_user_model()
    form_class=CustomUserCreationForm
    template_name='signup.html'
    success_url = reverse_lazy('login')

def login_func(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
            
        else:
            return render(request,'login.html',{'error':'ユーザ名、パスワードが間違っています'})

    return render(request,'login.html')


def logout_func(request):
    logout(request)
    return redirect('login')

class Chat(LoginRequiredMixin,generic.ListView):
    model=Room
    template_name='chat.html'
    context_object_name = 'room_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs).order_by('-created_at')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        partner_list=[]
        message_list=[]
        room_list=[]
        partner_dict={}
        user=CustomUser.objects.get(id=self.kwargs['user_id'])
        entries=Entries.objects.filter(user=user).order_by('-joined_at')
        for entry in entries:
            room_list.append(entry.room)

        for room in room_list:
            partner=room.room_member.all().exclude(id=user.id)[0]
            message_query=room.message_set.all()
            if message_query:
                message=message_query.order_by('-created_at')[0]
                message_list.append(message)
                partner_list.append(partner)

        partner_dict=dict(zip(partner_list,message_list)) 
        context['partner_dict']=partner_dict
        return context 


@login_required
def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    
    if request.user in room.room_member.all():
        Partner=room.room_member.all().exclude(id=request.user.id)[0]
        messages = Message.objects.filter(room=room).order_by('created_at')
        context = {
            'messages':messages,
            'room': room,
            'Partner':Partner,
            'WS_URL':settings.WS_URL,
        }
        return render(request,'chat_room.html',context)

    return redirect(reverse('Chat', args=[request.user.id]))

@login_required
def room(request,pk):
    User1=request.user
    User2=CustomUser.objects.get(pk=pk)
    roomQuery=Room.objects.filter(room_member=User1).filter(room_member=User2)
    if not roomQuery.exists():
        room = Room.objects.create()
        room.room_member.add(User1)
        room.room_member.add(User2)
    else:
        room=roomQuery[0]

    return redirect(reverse('chat_room', args=[room.id]))

def search_cat_video_on_youtube(request, keyword='猫 癒やし'):
    if request.method == 'GET':
        youtube_api_key = os.environ['YOUTUBE_API_KEY']
        youtube_url = 'https://youtube.com'
        
        try:
            videos_parameters_list = youtube.get_search(youtube_api_key, keyword)
            context = {
                'videos' : videos_parameters_list,
                'keyword' : keyword,
                'youtube_url' : youtube_url,
            }
            return render(request, 'youtube.html', context)
        except:
            error_message = 'リクエストにエラーが発生しました'
            context = {
                'error_message' : error_message,
                'keyword' : keyword,
            }
            return render(request, 'youtube.html', context)

class UserPageView(LoginRequiredMixin,generic.ListView):
    model=Post
    context_object_name = 'post_list'
    template_name='user_page.html'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        selected_user = CustomUser.objects.get(id=self.kwargs['pk'])
        queryset=queryset.filter(user=selected_user)
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        liked_list = []
        followed=False
        selected_user = CustomUser.objects.get(id=self.kwargs['pk'])
        selected_user_following_count=selected_user.following.count()
        selected_user_followed_count=selected_user.followed.count()
        following_list=self.request.user.following.all() 
        
        followed=following_list.filter(followed=selected_user)
        if followed.exists():
            followed=True

        _context={
            'selected_user_following_count':selected_user_following_count,
            'selected_user_followed_count':selected_user_followed_count,
            'selected_user':selected_user,
            'followed':followed,
        }
        context={**_context, **context}

        return context
