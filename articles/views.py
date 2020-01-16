from django.shortcuts import render
from articles.models import Article
from django.views.generic import ListView
# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
