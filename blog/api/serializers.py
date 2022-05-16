from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = "_all_"
    readonly = ["modified_at", "created_at"]

  