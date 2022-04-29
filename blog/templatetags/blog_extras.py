# convention to name the template tag files is to name them something_extras.py
"""
load custom template tag libraries into a template before using the build in 
load template tag. More than likely, you’ve loaded the static template tag library 
like this:{% load static %}

Django looks for template libraries to load inside Python files in the templatetags 
folder inside Django apps. The template library it loads is simply the name of the file.


Before the filter can be used, it needs to be registered into the template library. 
This is actually a three step process:
1. Import the django template module.
2. Create an instance of the django.template.Library class.
3. Register the filter function into the Library with its filter function.
"""

from django.contrib.auth import get_user_model
from django import template   # Step1: import django template


from blog.models import Post


# safe html
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()   #Step2, used to register custom templates and filters

user_model = get_user_model()


""" 
called the Library instance register, it makes it clear that the decorator is registering a filter.
The name of the filter in the template is automatically made the same as the name of the function, 
but this can be customized by passing a name argument to register.filter. 
For example, @register.filter(name="author_details")


safe html
To have good output that’s really safe, we need to first escape the dangerous parts of the text that we’re 
dealing with. Then, mark the whole string as safe so that only the HTML we trust is output verbatim.
Escaping strings is done with the django.utils.html.escape function. This will encode the HTML entities in a 
string. Once we have escaped only the dangerous values, we can mark a string as safe with the 
django.utils.safestring.mark_safe function. Once a string has been marked as safe, 
Django won’t escape it again when outputting in a template, so use with caution.


The django.utils.html.format_html is the preferred way of building HTML strings as it escapes values and 
marks strings safe in a single step. For example, when we build the opening <a> tag for the email link, 
we are escaping the email address on the line before and then putting it in the string. 
If we forgot to do the escape step, it could be dangerous.

So instead of creating the prefix like this:
email = escape(author.email)
prefix = f'<a href="mailto:{email}">'

We can do it in a single step:
prefix = format_html('<a href="mailto:{}">', author.email)
"""

# custom filter
@register.filter
def author_details(author, current_user=None):
  # Note the use of isinstance to check that we’re working with a User object, 
  # just in case someone has passed the wrong type of variable. 
  if not isinstance(author, user_model):
    return ""

  if author == current_user:
    return format_html("<strong>me</strong>")

  if author.first_name and author.last_name:
    # f string formatting
    name = escape(f"{author.first_name} {author.last_name}")
  else:
    name = escape(f"{author.username}")
  
  if author.email:
    email = escape(author.email)
    #prefix = f'<a href="mailto:{email}">'
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""
  
  return format_html("{}{}{}", prefix, name, suffix) # mark_safe(f"{prefix}{name}{suffix}")


#author_detail template tag with context enabled
# @register.simple_tag(takes_context=True)
# def author_details_tag(context):
#     request = context["request"]
#     current_user = request.user
#     post = context["post"]
#     author = post.author

#     if author == current_user:
#         return format_html("<strong>me</strong>")

#     if author.first_name and author.last_name:
#         name = f"{author.first_name} {author.last_name}"
#     else:
#         name = f"{author.username}"

#     if author.email:
#         prefix = format_html('<a href="mailto:{}">', author.email)
#         suffix = format_html("</a>")
#     else:
#         prefix = ""
#         suffix = ""

#     return format_html("{}{}{}", prefix, name, suffix)


# custom tag, simple_tag is the name of tag

#extra-classes can take other classes like that of bootstrap border-bottom in example
@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row">', extra_classes)

@register.simple_tag
def endrow():
  return format_html('</div>')


# output the opening and closing tags for a Bootstrap. 
# {} is the holder for other classes passed as argument.
@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")


"""
Include templates
This is very simple to implement, but its main drawback is that included templates can 
only access variables that are already in the including template’s context. That means
any extra variables need to be passed in from the calling view, so if it’s a template 
that’s used in lots of places you’ll be repeating the data-loading code in lots of 
different views.
By using an inclusion tag, you can query for extra data inside your template tag 
function, which can then be used to render a template.
Inclusion tags are registered with the Library.inclusion_tag function. 
This has one required argument, the name of the template to render. 
Unlike simple tags, inclusion tags don’t return a string to render. 
They return a context dictionary, which is used to render template used during 
registration.
"""

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]  # get last 5 after exclusion as they will be latest
  return {"title": "Recent posts", "posts":posts}
