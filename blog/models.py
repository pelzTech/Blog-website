from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  
    description_1 = models.TextField(blank=True, null=True)  
    media_1 = models.FileField(upload_to='blog_media/', blank=True, null=True)  
    description_2 = models.TextField(blank=True, null=True)  
    media_2 = models.FileField(upload_to='blog_media/', blank=True, null=True)  
    additional_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    ) 

    def __str__(self):
        return f"Comment by {self.author.username if self.author else 'Anonymous'} on {self.post.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  
    bio = models.TextField(blank=True, null=True)  
    website = models.URLField(blank=True, null=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return self.user.username
