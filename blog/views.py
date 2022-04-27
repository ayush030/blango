from django.shortcuts import render
from .models import Post
from django.utils import timezone
# Create your views here.

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()) #lte = less than equal to
    return render(request, "blog/index.html", {"posts": posts})
