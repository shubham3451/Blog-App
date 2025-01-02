from django.contrib import admin
from .models import MyUser, Profile, Post

# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display =     list_display = ('email', 'username', 'last_active', 'date_joined','date_modified','is_staff', 'is_active', 'is_admin',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'profile_pic','cover_pic', 'date_of_birth', 'phone',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
        list_display = ('author', 'content', 'post_type', 'date_posted', 'date_modified','image','video','audio','link',)