from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()), # CBV 포스트 목록 페이지
    # path('', views.index), # FBV 포스트 목록 페이지
    path('<int:pk>/', views.PostDetail.as_view()), # CBV 포스트 상세 페이지
    # path('<int:pk>/', views.single_post_page), # FBV 포스트 상세 페이지
]