#rest_framework.decorators.api_view makes FBV more comprehensive. A similar implementation for CBV is by the use of rest_framework.generics.<>APIView.

#rest_framework.mixins have REST implementation that can be leveraged in sub-classes. The rest_framework.generics.<>APIView has these mixins implemented.

# documentation- https://www.django-rest-framework.org/api-guide/generic-views/

from rest_framework import generics

from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer
from blog.models import Post
from blango_auth.models import User


#implementation DRF view bases permissions
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject


class PostList(generics.ListCreateAPIView):
  # get and post implementation together
  permission_classes = [IsAdminUser]
  
  queryset = Post.objects.all()
  serializer_class= PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  #  IsAdminUser always returns True from has_object_permission(), even if a user isn’t logged in! So by using it we’ll give all permissions to everyone.
  # permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

#get, post, delete implementation together
  queryset= Post.objects.all()
  serializer_class= PostDetailSerializer

# use this for token authentication
# requests.get("http://127.0.0.1:8000/api/v1/posts/", headers={"Authorization": "Token <token_val>"})

class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer