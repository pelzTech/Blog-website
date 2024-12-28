# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.post_create, name='post_create'),
    path('blog/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('blog/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),  
    path('subscribe/', views.subscribe, name='subscribe'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
