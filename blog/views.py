from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import CommentForm
# Create your views here.

import logging

#view caching or caching the response of the full page
from django.views.decorators.cache import cache_page

#cookie configuration
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
logger = logging.getLogger(__name__)

#accessing caches
# from django.core.cache import caches
# default_caches = caches.["default"]

from django.core.cache import cache
# cache is the equivalent of caches["default"]/our default_cache variable

#caches the response for 300 sec 
# @cache_page(300)
# @vary_on_headers("Cookie") #or vary_on_cookie
def index(request):
    # #demo for cache_page and cookie test
    # from django.http import HttpResponse
    # return HttpResponse(str(request.user).encode("ascii"))

    posts = Post.objects.filter(published_at__lte=timezone.now()) #lte = less than equal to

    logger.debug("Got %d posts", len(posts))
    
    cache.set(f"post_count", len(posts, 30)

    return render(request, "blog/index.html", {"posts": posts})



"""
First, we check if the user is active. Users who are inactive or aren’t logged in 
(anonymous users) will fail this test and default to having the comment_form variable
set to None.
we check the request method. If it’s not POST, a blank CommentForm is created.
if it’s valid, we’ll save the form, using the commit=False argument. 
This won’t write the Comment object to the database, instead it will return it. 
We need to do this to set the other attributes on the Comment before saving.
The Comment is then saved, and finally, we perform a redirect back to the current Post
"""

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()

                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    
    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})