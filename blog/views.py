from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# CBV 포스트 목록 페이지
class PostList(ListView):
    model = Post
    ordering = '-pk'

# FBV 포스트 목록 페이지
# def index(request):
#     # DB에 query 날리기
#     posts = Post.objects.all().order_by('-pk') # 최신 포스트부터 보여주기
#
#     return render(
#         request,
#         'index.html',
#         {
#             'posts': posts, # template으로 보내는 데이터(context)
#         }
#     )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )