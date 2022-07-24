from django.shortcuts import render
from .models import Post

def index(request):
    # DB에 query 날리기
    posts = Post.objects.all().order_by('-pk') # 최신 포스트부터 보여주기

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )