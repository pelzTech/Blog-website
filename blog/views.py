# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Comment
from .forms import CommentForm, PostForm

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_superuser

# Home page
def home(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/home.html', {'latest_posts': latest_posts})

# About page
def about(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/about.html', {'latest_posts': latest_posts})

# Services page
def services(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/services.html', {'latest_posts': latest_posts})

# Contact page
def contact(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/contact.html', {'latest_posts': latest_posts})

# Privacy Policy page
def privacy_policy(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/privacy_policy.html', {'latest_posts': latest_posts})

# List of blog posts
def blog_list(request):
    posts = Post.objects.all()
    latest_posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'blog/blog_list.html', {'posts': posts, 'latest_posts': latest_posts})

# Blog post detail view with comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

# Subscribe to newsletter
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        messages.success(request, "You've successfully subscribed to our newsletter!")
        return redirect('home')

# Create a new comment
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            parent_id = request.POST.get('parent_id')
            parent_comment = Comment.objects.get(pk=parent_id) if parent_id else None

            comment = Comment(
                post=post,
                author=request.user if request.user.is_authenticated else None,
                content=content,
                parent=parent_comment
            )
            comment.save()
            messages.success(request, "Your comment has been posted.")
        else:
            messages.error(request, "There was an error with your comment. Please try again.")

    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})

# Admin-only comment deletion
@login_required
@user_passes_test(is_admin)
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})

# Placeholder views for creating, editing, and deleting posts
@login_required
@user_passes_test(is_admin)
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog_list')
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
