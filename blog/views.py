from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag

# CBV 포스트 목록 페이지(ListView)
class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


# CBV 포스트 상세 페이지(Detail View)
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# FBV 카테고리 페이지
def category_page(request, slug):
    # slug 인자로 'no_category'가 넘어오는 경우 예외 처리
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )

# FBV 태그 페이지
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all() # FK tag 필드로 연결된 모든 post 목록

    return render(
        request,
        'blog/post_list.html',
        # context
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )

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

# FBV 포스트 상세 페이지
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
# 
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )