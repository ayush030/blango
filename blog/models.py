from django.db import models
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



# Create your models here.
class Tag(models.Model):
  value = models.TextField(max_length=100, unique=True)

  def __str__(self):
    return self.value
    

class Comment(models.Model):
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.TextField()
  
  #the comment can be on a author or a post
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  
  #to get value of the pk of the said content_object.  PK of the related object(Post or User)
  object_id = models.PositiveIntegerField(db_index=True)

  # its a foreign key to generic object with mapping to its ContentType and its pk 
  content_object = GenericForeignKey("content_type", "object_id")

  created_at = models.DateTimeField(auto_now_add = True, db_index=True)
  modified_at = models.DateTimeField(auto_now = True)

  def __str__(self):
    return self.creator



class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  published_at = models.DateTimeField(blank=True, null = True, db_index=True)
  title = models.TextField(max_length=100)
  
  #SlugField in Django is like a CharField, where you can specify max_length attribute also. 
  #If max_length is not specified, Django will use a default length of 50. 
  slug = models.SlugField(unique=True)

  summary = models.TextField(max_length=500)
  content = models.TextField()
  tags = models.ManyToManyField(Tag, related_name="posts")

  comments = GenericRelation(Comment)

  
  def __str__(self):
    return self.title

class AuthorProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
  bio = models.TextField()

  def __str__(self):
    return f"{self.__class__.__name__} object for {self.user}"
