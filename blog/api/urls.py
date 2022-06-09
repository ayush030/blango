from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

# from .views import PostList, PostDetail
from blog.api.views import UserDetail, TagViewSet, PostViewSet
import rest_framework.urls

#for auth token
from rest_framework.authtoken import views

#for swagger UI
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os


#routers for viewset
from rest_framework.routers import DefaultRouter


urlpatterns= [
  # added viewsets for Post hence, omitted urls for individual post views. Router and endpoint are defined below
  # path('posts/',  PostList.as_view(), name='api_post_list'),
  # path('posts/<int:pk>', PostDetail.as_view(), name="api_post_detail"),
  path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
  ]


#schema view for drf swagger UI using drf_yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/",
    public=True,
)

# DRF login pages and swagger UI
urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

#to retrieve json information of the models.  DRF will detect that you have the login URL configured and automatically add a link to log in in the top right corner of a DRF view page.
# urlpatterns= format_suffix_patterns(urlpatterns)

#registering viewsets for endpoint of TagViewSet 
router = DefaultRouter()

router.register("tags", TagViewSet)     #here tags is the endpoint url
router.register("posts", PostViewSet)

urlpatterns += [
    path("", include(router.urls)),
    path("posts/by-time/<str:period_name>/", PostViewSet.as_view({"get": "list"}), name="posts-by-time",),
]
