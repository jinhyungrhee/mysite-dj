from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author : 추후 작성 예정

    # admin Post 목록에 제목 나타내기
    def __str__(self):
        return f'[{self.pk}]{self.title}'

    # 모델의 레코드별 URL 생성 규칙 정의
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
