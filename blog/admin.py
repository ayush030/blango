from django.contrib import admin
from .models import Post, Tag, Comment
# Register your models here.



"""To configure how the admin site behaves with a certain model, a subclass of admin.ModelAdmin 
must be created. This subclass’s attributes determine how the model is displayed. 
First let’s look at how we’ll create one, for the Post model."""

#PostAdmin shall govern how the admin page shall display the information pertaining to Post
class PostAdmin(admin.ModelAdmin):
  # slug field shall be pre-populated based on title field
  prepopulated_fields = {"slug" : ("title",)}
  
  # at admin->post page it shall display the below two fields
  list_display = ("slug", "published_at")

"""Here we’re setting just one attribute, prepopulated_fields. 
When used in this way, some JavaScript is inserted into the admin page so that the slug field 
updates when the title field changes. It will automatically “slugify” the title. 
But, there are many other ways to customise the ModelAdmin."""

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
