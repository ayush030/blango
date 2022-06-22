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

from django.db.models import Q
from django.utils import timezone

from datetime import timedelta
from django.http import Http404

#filtering by django-filter.rest_framework
from .filters import PostFilterSet

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
  filterset_class = PostFilterSet 

  # By default, all readable serialized fields are available for ordering
  ordering_fields = ["published_at", "author", "title", "slug"]

  filterset_fields = ["author", "tags"]

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
    
    # applying pagination to mine method - user defined viewset method
    page = self.paginate_queryset(posts) # adds paging paraphernalia to the existing queryset
    if page is not None:
      serializer = PostSerializer(page, many=True, context={"request": request})
      return self.get_paginated_response(serializer.data)
    
    serializer = PostSerializer(posts, many=True, context={"request":request})
    return Response(serializer.data)
  


  # Since the list of Posts now changes with each user, we need to make sure we add the vary_on_headers() decorator to it, with Authorization and Cookie as arguments
  def get_queryset(self):
    if self.request.user.is_anonymous:
      queryset = self.queryset.filter(published_at__lte=timezone.now())
    
    elif self.request.user.is_staff:
      queryset = self.queryset
    
    else:
      queryset = self.queryset.filter(Q(published_at__lte=timezone.now()) | Q(author = self.request.user))

    time_period_name = self.kwargs.get("period_name")

    if not time_period_name:
      return queryset
    
    if time_period_name == "new":
      return queryset.filter(published_at__gte= timezone.now()- timedelta(hours=1))
    elif time_period_name == "today":
      return queryset.filter(published_at__date=timezone.now().date(),)
    elif time_period_name == "week":
      return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
    else:
      raise Http404(f"Time period {time_period_name} is not valid, should be " f"'new', 'today' or 'week'")
  
  # adding caching to methods implemented/available with viewset by passthrough same methods using super class
  @method_decorator(cache_page(120))
  @method_decorator(vary_on_headers("Authorization", "Cookie"))
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
    
    # applying pagination to mine method - user defined viewset method
    page = self.paginate_queryset(tag.posts)  # adds paging paraphernalia to the existing queryset
    if page is not None:
      post_serializer = PostSerializer(page, many=True, context={"request":request})
      return self.get_paginated_response(post_serializer.data)

    # Since PostSerializer uses a HyperlinkRelatedField it needs access to the current request so we need to pass that in a context dictionary. 
    post_serializer = PostSerializer(tag.posts, many=True, context={"request":request})
    #--------------------how tag.posts is retrieved: from the name field set in the models-------------------------------
    return Response(post_serializer.data)


  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
    return super(TagViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(300))
  def retrieve(self, *args, **kwargs):
    return super(TagViewSet, self).retrieve(*args, **kwargs)
