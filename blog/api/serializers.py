from rest_framework import serializers
from blog.models import Post, Tag, Comment
from blango_auth.models import User


class TagField(serializers.SlugRelatedField):
  def to_internal_value(self, data):
    try:
      return self.get_queryset().get_or_create(value=data.lower())[0]
    except(TypeError, ValueError):
      self.fail(f"Tag value {data} is invalid")


class PostSerializer(serializers.ModelSerializer):
  tags =TagField(
        slug_field="value", many=True, queryset=Tag.objects.all()
    )
  author = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(), view_name="api_user_detail", lookup_field="email"
    )
  
  class Meta:
    model = Post
    fields = "__all__"
    readonly = ["modified_at", "created_at"]


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "email"]


class CommentSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False) #if its a new comment this will be empty
  creator = UserSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ["id", "creator", "content", "modified_at", "created_at"]
    read_only = ["modified_at", "created_at"]


class PostDetailSerializer(PostSerializer):
  comments = CommentSerializer(many=True)

  def update(self, instance, validated_data):
    comments = validated_data.pop("comments")

    #post instance to be saved besides comments(as they have been popped/removed)
    instance = super(PostDetailSerializer, self).update(instance, validated_data)

    for comment_data in comments:
      if comment_data.get("id"):
        continue
      
      #for new comments
      comment = Comment(**comment_data)
      comment.creator = self.context["request"].user    # request shall be available in self.context for the present instance
      comment.content_object = instance
      comment.save()

    return instance
