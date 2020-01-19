from django.contrib import admin
from articles.models import Article
from comments.models import Comment
# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title','date','author']
    inlines = [
        CommentInline
    ]

admin.site.register(Article, ArticleAdmin)
