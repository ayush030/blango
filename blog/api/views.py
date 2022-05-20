#rest_framework.decorators.api_view makes FBV more comprehensive. A similar implementation for CBV is by the use of rest_framework.generics.<>APIView.

#rest_framework.mixins have REST implementation that can be leveraged in sub-classes. The rest_framework.generics.<>APIView has these mixins implemented.

# documentation- https://www.django-rest-framework.org/api-guide/generic-views/

from rest_framework import generics

from blog.api.serializers import PostSerializer
from blog.models import Post

class PostList(generics.ListCreateAPIView):
  # get and post implementation together
  queryset = Post.objects.all()
  serializer_class= PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  #get, post, delete implementation together
  queryset= Post.objects.all()
  serializer_class= PostSerializer

# use this for token authentication
# requests.get("http://127.0.0.1:8000/api/v1/posts/", headers={"Authorization": "Token <token_val>"})
