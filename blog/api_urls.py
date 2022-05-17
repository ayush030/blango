from django.urls import path

from blog.api_views import post_list, post_detail

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("posts/", post_list, name="api_post_list"),
    path("posts/<int:pk>", post_detail, name="api_post_detail"),
#  trailing / on the post_detail URL has been removed – otherwise we’d end up having URLs like /api/v1/posts/5/.json.
]


urlpatterns = format_suffix_patterns(urlpatterns)
# DRF examining the request Accept header, the header that specifies what type of content it will accept. But DRF allows us to make a couple of changes to be able to control the content type using a file extension. This means we could request JSON data for a Post with a URL like http://127.0.0.1:8000/api/v1/posts/5.json, even from a browser.