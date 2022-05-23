from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PostList, PostDetail, UserDetail
import rest_framework.urls

#for auth token
from rest_framework.authtoken import views

urlpatterns= [
  path('posts/',  PostList.as_view(), name='api_post_list'),
  path('posts/<int:pk>', PostDetail.as_view(), name="api_post_detail"),
  path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]

# DRF login pages
urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token)
]

#to retrieve json information of the models.  DRF will detect that you have the login URL configured and automatically add a link to log in in the top right corner of a DRF view page.
urlpatterns= format_suffix_patterns(urlpatterns)