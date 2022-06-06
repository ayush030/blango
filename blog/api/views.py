#rest_framework.decorators.api_view makes FBV more comprehensive. A similar implementation for CBV is by the use of rest_framework.generics.<>APIView.

#rest_framework.mixins have REST implementation that can be leveraged in sub-classes. The rest_framework.generics.<>APIView has these mixins implemented.

# documentation- https://www.django-rest-framework.org/api-guide/generic-views/

from rest_framework import generics

from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag
from blango_auth.models import User


#implementation DRF view bases permissions
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject


#viewsets for Tag
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


#caching to viewsets or generic class based views( use of method_decorator)
#  The method_decorator decorator transforms a function decorator into a method decorator so that it can be used on an instance method.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied 

#generic implementation using APIView 

# class PostList(generics.ListCreateAPIView):
#   # get and post implementation together
#   permission_classes = [IsAdminUser]
  
#   queryset = Post.objects.all()
#   serializer_class= PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#   #  IsAdminUser always returns True from has_object_permission(), even if a user isn’t logged in! So by using it we’ll give all permissions to everyone.
#   # permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
#   permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

# #get, post, delete implementation together
#   queryset= Post.objects.all()
#   serializer_class= PostDetailSerializer

# use this for token authentication
# requests.get("http://127.0.0.1:8000/api/v1/posts/", headers={"Authorization": "Token <token_val>"})



# implementating viewset based Post views
class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer
  
  @method_decorator(cache_page(300))
  @method_decorator(vary_on_headers("Authorization"))
  @method_decorator(vary_on_cookie)
  #method_decorator(vary_on_headers("Authorization", "Cookie"))  #alternatively
  @action(methods=["get"], detail=False, name="Posts by the logged in user")
  def mine(self, request):
    if request.user.is_anonymous:
      raise PermissionDenied("You must be logged in to see which Posts are yours")
    posts = self.get_queryset().filter(author=request.user)
    serializer = PostSerializer(posts, many=True, context={"request":request})
    return Response(serializer.data)
  
  # adding caching to methods implemented/available with viewset by passthrough same methods using super class
  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
    return super(PostViewSet, self).list(*args, **kwargs)


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
      return super(UserDetail, self).get(*args, **kwargs)


#Tag viewset

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

# methods: A list of HTTP methods that the action will respond to. Defaults to ["get"].
# detail: Determines if the action should apply to detail requests (if True) or list (if False). This argument is required.
# url_path: Manually specify the path to be used in the URL. Defaults to the method name (e.g. posts).
# url_name: Manually specify the name of the URL pattern. Defaults to the method name with underscores replaced by dashes. The full name of our method’s URL is tag-posts.
# name: A name to display in the Extra Actions menu in the DRF GUI. Defaults to the name of the method.
  
  @action(methods=["get"], detail=True, name="Posts with the tag")
  def posts(self, request, pk=None):
    # We have access to the pk from the URL, so we could fetch the Tag object from the database ourselves. However, the ModelViewSet class provides a helper method that will do that for us – get_object() – so we use that instead.
    tag = self.get_object()

    # Since PostSerializer uses a HyperlinkRelatedField it needs access to the current request so we need to pass that in a context dictionary. 
    post_serializer = PostSerializer(tag.posts, many=True, context={"request":request})
    #--------------------how tag.posts is retrieved-------------------------------
    return Response(post_serializer.data)


  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
    return super(TagViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(300))
  def retrieve(self, *args, **kwargs):
    return super(TagViewSet, self).retrieve(*args, **kwargs)
