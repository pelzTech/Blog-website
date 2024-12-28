from django.contrib import admin
from .models import Post, Comment, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at') 
    search_fields = ('title', 'content', 'description_1', 'description_2')  # Allow searching by title or content
    list_filter = ('author', 'created_at')  
    readonly_fields = ('author',)  

    def save_model(self, request, obj, form, change):
        if not change:  
            obj.author = request.user  
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'content')  
    search_fields = ('content', 'author__username') 
    list_filter = ('created_at',)  

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'view_avatar', 'bio', 'website', 'phone_number')  
    search_fields = ('user__username', 'bio', 'phone_number') 

    def view_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50" />')  
        return "No Avatar"
    view_avatar.short_description = 'Avatar'

   
    def save_model(self, request, obj, form, change):
        if not obj.avatar and not change:  
            obj.avatar = "default-avatar.jpg" 
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
