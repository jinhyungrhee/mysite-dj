from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.PostCreate.as_view()), # 포스트 작성 페이지
    path('tag/<str:slug>/', views.tag_page), # 태그 페이지
    path('category/<str:slug>/', views.category_page), # 카테고리 페이지
    path('', views.PostList.as_view()), # CBV 포스트 목록 페이지
    # path('', views.index), # FBV 포스트 목록 페이지
    path('<int:pk>/', views.PostDetail.as_view()), # CBV 포스트 상세 페이지
    # path('<int:pk>/', views.single_post_page), # FBV 포스트 상세 페이지
]