from django.db import models
from articles.models import Article
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE,related_name='comments')
    comment = models.CharField(max_length=140)
    author =  models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')