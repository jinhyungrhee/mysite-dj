from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self): # 외부에 나타나는 이름/제목
        return self.name

    # Slug 필드를 사용하여 고유 URL 생성
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True ,on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    # 외부에 나타나는 이름/제목(admin Post 목록 포함)
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    # 모델의 레코드별 URL 생성 규칙 정의
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    # 첨부 파일명 반환
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 첨부 파일 확장자명 반환
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

