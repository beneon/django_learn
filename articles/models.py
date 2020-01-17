from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    body = models.TextField(verbose_name='内容')
    date = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='作者'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

