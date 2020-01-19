from django.contrib import admin
from comments.models import Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['comment','article','author']

admin.site.register(Comment, CommentAdmin)
