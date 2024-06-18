from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models_nakagawa import *
from .models_nishio import *

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    list_display = ['email','username','ProfileImage']

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('ProfileImage',)}),
    )

    add_fieldsets = (
        (None,{
            'fields':('email','username','password1','password2')
        }),
    )


class MemberInlineAdmin(admin.TabularInline):
    model = Room.room_member.through

class RoomAdmin(admin.ModelAdmin):
    inlines = (MemberInlineAdmin,)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Message)
admin.site.register(Entries)
admin.site.register(Post)
admin.site.register(Comment)

