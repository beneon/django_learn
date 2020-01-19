# django form的学习笔记

参考[django中使用form的教程](https://docs.djangoproject.com/en/3.0/topics/forms/)

进一步阅读：

- [form api](https://docs.djangoproject.com/en/3.0/ref/forms/api/)
- [form fields](https://docs.djangoproject.com/en/3.0/ref/forms/fields/)
- [form field validation](https://docs.djangoproject.com/en/3.0/ref/forms/validation/)

## 笔记

1. forms in django > django form class: A form’s **fields** are **themselves classes**
2. forms in django > instantiating, processing and rendering forms: When we’re dealing with a form we typically **instantiate it in the view**.
3. 目前看来我们用的最多的还是modelform

---

# model form 笔记

[来源](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/)

```python
>>> from django.forms import ModelForm
>>> from myapp.models import Article

# Create the form class.
>>> class ArticleForm(ModelForm):
...     class Meta:
...         model = Article
...         fields = ['pub_date', 'headline', 'content', 'reporter']

# Creating a form to add an article.
>>> form = ArticleForm()

# Creating a form to change an existing article.
>>> article = Article.objects.get(pk=1)
>>> form = ArticleForm(instance=article)
```

注意到这里有个instance的参数, 是一个来自model的记录

## fields

form field基本和model field相对应.

-    ForeignKey is represented by django.forms.ModelChoiceField, which is a ChoiceField whose choices are a model QuerySet.
-    ManyToManyField is represented by django.forms.ModelMultipleChoiceField, which is a MultipleChoiceField whose choices are a model QuerySet.

书中使用

```python
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body') # new
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)
```

可以看到这里是用form_valid的override

而文档里面:

```python
form = PartialAuthorForm(request.POST)
author = form.save(commit=False)
author.title = 'Mr'
author.save()
```

这里用的是save(), commit为false的版本. commit为false以后,save()返回的是一个对象, 这时候可以给对象做一些进一步的操作,最后再save()

**需要注意的是**: 书中是从view的角度, 而文档是从form的角度.

fields方面, 除了用()枚举以外, 还可以用__all__来表示全部, 然后用exclude替代fields属性剔除不需要的field

---

# on bootstrap

