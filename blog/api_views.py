import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post

from blog.api.serializers import PostSerializer

# decorators of DRF, it automatically rejects unsupported methods by returning a response with a 405 status code. We no longer have to return HttpResponseNotAllowed ourselves.
from rest_framework.decorators import api_view

#response from DRF, It handles the DRF Response object, returning different responses based on what the client wants.
from rest_framework.response import Response

# def post_to_dict(post):
#     return {
#         "pk": post.pk,
#         "author_id": post.author_id,
#         "created_at": post.created_at,
#         "modified_at": post.modified_at,
#         "published_at": post.published_at,
#         "title": post.title,
#         "slug": post.slug,
#         "summary": post.summary,
#         "content": post.content,
#     }


@csrf_exempt 
@api_view(["GET", "POST"])
def post_list(request, format=None):
    if request.method == "GET":
        posts = Post.objects.all()
        # posts_as_dict = [post_to_dict(p) for p in posts]
        #JsonResponse({"data": posts_as_dict})
        
        # return JsonResponse({"data": PostSerializer(posts, many=True).data})

        return Response({"data": PostSerializer(posts, many=True).data})

    elif request.method == "POST":
        # post_data = json.loads(request.body)
        #post = Post.objects.create(**post_data)
        # serializer = PostSerializer(data=post_data)

        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        # return HttpResponse(
        #     status=HTTPStatus.CREATED,
        #     headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        # )

        return Response(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    #return HttpResponseNotAllowed(["GET", "POST"]) # not required due to api_view
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk, format=None):
    # post = get_object_or_404(Post, pk=pk)
    try:
      post=Post.objects.get(pk=pk)
    except:
      return Response(status=HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        # return JsonResponse(post_to_dict(post))
        # return JsonResponse(PostSerializer(post).data)
        return Response(PostSerializer(post).data)
    elif request.method == "PUT":
        post_data = json.loads(request.body)
        # for field, value in post_data.items():
        #     setattr(post, field, value)
        # post.save()
        
        serializer = PostSerializer(post, data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return HttpResponse(status=HTTPStatus.NO_CONTENT)

        return Response(status=HTTPStatus.NO_CONTENT)
    elif request.method == "DELETE":
        post.delete()
        # return HttpResponse(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.NO_CONTENT)

    # return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])  # removed due to decorator api_view