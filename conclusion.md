# Django for beginners 学习笔记

> 书本链接在[这里](https://djangoforbeginners.com/)，书不便宜，也不好说就真的值这个价钱，但是作为入门读物确实是好书。请尊重知识产权自行购买

这本书刚买回来的时候读了一遍也照着程序自己写了一次，但是始终觉得没有学通，这次再读一次，觉得可以做一个总结了。

## 书中内容的基本思路

1. 搭框架，startproject， startapp 两个命令
2. 利用class based views建立一个app，不涉及database（TemplateView)
3. 建立一个涉及database的app, 单页面，只有list
4. 建立一个有list以及detail view的涉及database的app。
5. 建立一个实现增删查改的app，引入form

## django开盘基本套路

1. `django-admin startproject project名称 .`。这里面django-admin是安装django以后就有的一个命令行工具，startproject是开始新的项目的命令，project名称自定，点号表示在当前目录新建项目，而不是额外再建一个文件夹
2. `python manage.py startapp app名称`
3. `settings.py`的常规设置，包括但不限于：
    1. INSTALLED_APPS
    2. TEMPLATES.DIRS
    3. LANGUAGE_CODE, 一般设置为zh-hans
    4. TIME_ZONE = 'Asia/Chongqing'
    5. STATICFILES_DIRS，LOGIN_REDIRECT_URL，LOGOUT_REDIRECT_URL
    6. 如果按照该书的方式以custom user model扩展用户模型，还需要AUTH_USER_MODEL
    7. 使用crispy forms优化form，如果用的不是默认的bootstrap2，就需要额外设置CRISPY_TEMPLATE_PACK
    8. EMAIL_BACKEND需要设置，供发送transactional email使用。在dev阶段可以用`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
4. 要像书里一样用custom user model，**在第一次migration以前**就要把custom user model给写好。

## model

Django以对象的形式呈现数据库。编程的时候很少会碰sql，基本是通过model这一个层次去访问数据。

- 一个class对应一个表
- class中的各项对应表中的各个field
- 有很多pythonic的特性，比如`__str__`
- get_absolute_url应该定义一下

### 关于many2one

要弄数据库，肯定要有foreingkey。ForeignKey是django中建立many2one的一种field。这个field肯定是存在与many这一端，为什么呢？因为一个field只能有一个值呀，如果放在one这一端的话，那一个格子就要放many的值了。

[关于database的一些常识性的内容](https://wsvincent.com/database-design-tutorial-for-beginners/)

## url-view-template 轴

话说回来， django for beginners这本书在views这一块基本上对function based views着墨不多，主要的篇幅都在使用class based views。而与之相对的，[Mozilla的教程](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)以及[Django自家的教程](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)则是更注重function based views。另外我发现这本书基本上没有提到form，和form有关的python编码很多时候都是隐藏在views里面了。

我觉得Mozilla的教程还有Django自家的教程还是很有必要去看的。但是话说回来，跟着这本书从头到尾用class based views做下来，好像也没什么不对头的地方。

说回正题，url-views-template这三个东西是紧密相连的。url定义路由，也就是如何触发views，然后template决定如何将views的数据呈现出来，当然也包括如何定义一个form，然后通过views向数据库提交数据。所以这是一个用户（提交url）到服务器（路由根据url找到对应资源，触发相应views，传回数据以template渲染），再到用户（将渲染好的网页交给用户）的过程

### url

url一般分成两个层级定义：

1. 项目层级。在项目文件夹里有一个自建的`urls.py`，当然你整个项目就这一个路由文件也没毛病，但是一般这个级别的`urls.py`里面的urlpatterns只负责将各个app的url纳入总体路由机制，至于具体的资源定位那是各个app的事情。比如下面的`urls.py`：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('users/',include('django.contrib.auth.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('articles/',include('articles.urls')),
    path('comments/',include('comments.urls')),
    path('',include('pages.urls')),
]
```

include类型的path定义往往都是先给一个url string，然后附上include()，其参数是`app名.urls`。注意到上面有两个users，然后accounts和users都指向了`django.contrib.auth.urls`。这些写法多少还是有些monkey patching的嫌疑呢……

2. app层级，这个级别的urls就要和views相结合了

之前一直都不大明白django的import是怎么回事，比如说在下面的`urls.py`里面


```python
from django.urls import path
from articles.views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleCreateView,
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/',ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
```

实际上第二行的代码书里面经常用 `from .views import ...`的形式，这个`.`就经常让我很疑惑，实际上点号在这里代表的是同一文件夹（或者说是同一个package？毕竟文件夹里面有个__init__.py）, 那比如说现在我想导入pages 这个app的views怎么办呢？`pages.views`就可以了

上面的urlpatterns的定义方式是一个url string跟着一个view来定义的。因为用到的都是class based views，所以都有一个as_view()返回一个view function(?)，另外也都定义了name，这样方便后面用reverse来找。name起的都很有app的特征，毕竟在整个project里面这些名字都是可以用的，乱起名字容易重名。

另外像`<int:pk>/edit/`这样的url地址是包含参数的。这里的参数一般就是一个记录的id（或者主键），于是最后的url应该就是'articles/2/edit'这样的格式，这其中的2就会作为参数传入ArticleDetailView了。DetailView需要这个参数去返回特定的一个记录

而在template里面，pk这个参数是通过下面的方式起作用的

```html
<a href="{% url 'blog_detail' blog.pk %}">{{blog.title}}</a>
```

### views

就像前面说的，这本书主要都是用class based views。这种做法好处就是简单，坏处么……那么大一个黑箱，真的打开来以后就很晕。

## list+detail的app

### static files

**settings.py**: `STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]`

如果是load css， `{% load static %}`应该放在<!DOCTYPE html>和<html>之间

### blog detail

detail view的实现过程中，有以下细节：

1. template方面，list模板要有指向各个detail的链接
2. url方面，要定义指向各个detail的链接

整体而言pk是这个指定的核心。urls里是使用：

```
path('blog/<int:pk>',BlogDetailView.as_view(), name='blog_detail'),
```

而在list的template里面：

```html
<a href="{% url 'blog_detail' blog.pk %}">{{blog.title}}</a>
```

注意url这个tag的用法，先是url，然后是路由的名称，在之后是交给这个路由的参数blog.pk

为什么要用blog呢？用object也是可以的，但是最好就是直接在views里面通过context_object_name显示定义一下。

### testing

1. 早前编程的时候，在`on_delete = models.TextField`这里写错了，应该是`on_delete = models.CASCADE`。有意思的是就算代码修改过了以后，重新运行makemigrations还是会报错。这是因为某些奇怪的原因，当时代码写错的时候makemigrations没有被检查出来，已经写进了migration file了。这样一来就需要将blog这个app里面migrations文件夹下的错误文件删除，然后再makemigrations
2. 在template里面，没办法很好的使用python语言，但是在python代码内部就不一样了。比如说这个地方：`self.client.get('/post/1/')`，这是使用url定义的规则：`'blog/<int:pk>'`触发BlogDetailView。但是就像其他path定义的url一样，也可以使用reverse()来生成地址。所以除了写`/post/1`这样的地址，用`reverse('blog_detail',kwargs={'pk':1})`也是可以的。
3. 在model里面指向user的author项目是以ForeignKey的形式声明的。书中使用的是'auth.User'这个字符串。不过到了test中，使用的又是django.contrib.auth.get_user_model获取User的model。说不定在model里面也可以使用get_user_model来指向User。
4. query：`ModelName.objects.get(what = what)`。如果要新建一个entry，可以使用`Modelname.objects.create(what = what)`

## 增删改

### 增：

1. 在base template里面，给nav标签添加一个div，里面的链接指向name为blog_new的url。
2. 在url里面定义这个name为blog_new的url，指向BlogCreateView
3. 在views里面定义这个BlogCreateView。属于generic class based view，从`django.views.generic.edit`导入`CreateView`
    1. 除了传统的model，template_name以及可选的context object name以外，书里还定义了fields这个选项
4. 该编写create view对应的template了
    1.  `<form></form>之间填写form内容`
    2. form的action为空，method为post
    3. 在form的内部要放置`{% csrf_token %}`
    4. {{form.as_p}}将model有关的fields（在views里面用fields项做了额外的定义）用p标签的形式遍历写出来
    5. `<input type="submit" value="保存"/>`这个是标配
6. 这个时候提交form会返回错误，如果在shell里面测试一下就会知道，实际上数据这个时候已经进了数据库了。
    1. 话说回来，当时设计model的时候真的应该加入一个timestamp。
    2. 报错应该是`No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.`，说明需要提供一个redirect的地址。这个可以通过定义get_absolute_url来搞定，给model定义一个函数吧。
    3. 书中使用的函数定义是`return reverse('blog_detail',args=[str(self.id)])`，这也是一种写法
    
### 改

1. views中，是基于内置的UpdateView做subclass，explicit声明只给出title和body两个field
    1. 如果要输出所有fields，那可以用'__all__'
2. template方面form的method**还是**post
3. 继续使用form.as_p
4. 定义urls: `blog/<int:pk>/edit`

### 删

1. template方面没什么特别的，就是做一个确认页面，显示一下blog的内容，标题，然后加一个input，submit type。form的method仍旧是post……
2. views方面使用DeleteView，除了定义`model`,`template_name`以外，还需要定义一个`success_url`这个使用reverse_lazy定义

    > We use reverse_lazy as opposed to just reverse so that it won’t execute the URL redirect until our view has finished deleting the blog post.

### 测试

1. 除了有self.client.get，还有self.client.post对吧。post的第一个参数和get一样是地址，然后还要给第二个参数：post的data，以dict形式提供
2. update的client.post()里，path部分不止要给url name，还要给args。这里直接使用了转化成字符串的数值'1'。update以后默认是跳转，所以status code应该是302，而不是200
3. delete使用client.get()而不是post()
4. 说实话，这个地方应该还需要修正一下，因为它实际上用了几个不同的url路径来实现一个资源的不同动作

## 用户账号管理

1. auth是一个app，django自己提供的。
2. auth的User对象包含
    1. 用户名
    2. 密码
    3. 邮箱
    4. 名
    5. 姓
3. 用auth可以实现log in， log out还有sign in。其中sign in又包含了密码管理（修改，重置等）

### 登录

1. auth是自带的app，不过既然要用app肯定要在project的url里面记上一笔：`path('accounts/',include('django.contrib.auth.urls')),`
2. template方面，django会寻找registration这个文件夹。看到这里，我把settings.py里面TEMPLATES.DIRS只保留`os.path.join(BASE_DIR,'templates')`好像也是work的哦，因为Django会自动去文件夹里面找app名称的子文件夹嘛
3. login的template里面和前面增删查改的template很相似，也是写一个form，这里使用post方法，然后里面的内容利用`{{form.as_p}}`生成
4. 不需要写views，models，app内部的urls也不用
5. 在settings.py还需要加上一笔：`LOGIN_REDIRECT_URL = 'home'`。这里的home指的是url的name，我们可以用blog_list替代

> 其实这个`LOGIN_REDIRECT_URL = '/accounts/profile/'`在global setting里面是有的。不过我们还是自己写一下比较好

这个地方Django帮忙做的东西有点多，真的不大适应

6. 当然，base template还需要修改一下，把login放进来，不能总是用url直接访问。另外在登录以后也应该显示用户已经登录了。

### 首页更新

1. {% if user.is_authenticated %}可以判断是否已经登录
2. {{ user.username }}可以显示用户名

就像前面说的，auth是django自己提供的一个app。这个app的代码可以在django/contrib/auth里面看到。而在auth文件夹里，看看[urls.py](C:\ProgramData\Anaconda3\Lib\site-packages\django\contrib\auth\urls.py)

```python
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
```

而这些name都是可以直接在template里面使用的。

3. logout 之后去哪里呢？这个需要在setting里面设置

### 注册

注册是一个问题。书中是新建了一个app来专门负责这个事情。毕竟一个注册系统要提供这些功能页面：

1. 建立账号
2. 修改密码
3. 密码重设
4. 以及若干的确认页面和功能页面

也就是说上面auth的url中除了login和logout以外的所有url指向的页面都要做一个出来。不过本身这些url指向的view也可以作为参考 

startapp以后，首先要在settings里面添加记录，然后project的urls也要添加。这里有一个细节：

```python
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls')),
```

上面一行是在写login的时候加入的，是为了使用django自带的app，而下面的一行则是刚刚加入的。django会从上到下应用url规则。所以当我们申请accounts/signup的时候，第一个的规则没有适配项，这样就会用第二条规则，于是就使用了我们新建的app了

为什么signup没有呢？源码里面就是没有呀

#### view

view方面需要用到django自带的UserCreationForm，这个form自带username，password1和password2三个field。

CreateView之前在blogs里面也用过，不过那个时候的代码是这样的：

```python
class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog_create.html'
    context_object_name = 'blog'
    fields = ['title','author','body']
```

可以看到自己定义了model以及fields。但是在我们这里，转而使用的是form_class

```python
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
```

#### 模板

到了模板这里，想起来之前我们建立了一个registration的template。话说回来我们干嘛要建立这么一个template呢？尤其是考虑到它只用了一次，还是给login用的，而到了真正的signup的时候，我们又不用这个了…… 还是那句话，源码里面大量的template_name都是指向`registration/...`

虽然现在新建了一个accounts的app，template name也设置了，但是这边的template folder还是直接从templates里面搜，没有把accounts作为一个folder去搜索呢。区别到底在哪里呢？

---

# 自定义用户模型

1. 暂时先不migrate
2. 注意settings：
    1. INSTALLED_APPS
    2. AUTH_USER_MODEL
    3. LOGIN_REDIRECTED_URL, LOGOUT_REDIRECTED_URL
    4. STATICFILES_DIRS   
3. model中新建CustomUserModel
    custom user model基于 abstract user生成
4. form中新建UserCreationForm和UserChangeForm
    分别代表两种访问user model的方式：新建以及修改（供超级用户）
5. 将model和form在admin中注册
6. makemigrations, migrate
6. 建立superuser

## notes

1. model的fields和关于一个model的form的fields不一定是一模一样的。比如user model可以包含很多内容，但是注册form只需要username，email和password就够了
2. 这里继承的UserCreationForm，UserChangeForm都是继承于forms.ModelForm。ModelForm要求关于fields和model的各种设置放在Meta subclass里面。这样可以避免名称冲突。参见[Stack Overflow](https://stackoverflow.com/a/39476404)以及[document](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/)
3. 而CustomUserAdmin，继承UserAdmin（这个则继承于admin.ModelAdmin)，不用通过Meta设置。在CustomUserAdmin中，目前先针对add_form，form还有model做一个设置
4. 在makemigrations以及migrate以后，仍旧还能够对CustomUser添加fields，这个是可以的

---

# 用户登录

之前的*用户账号管理*部分也对登录、注册的机制做了一些常识，这里是在完成了custom user model以后，更全面的一个编码

## templates

1. 主要的template都在registration目录
2. 大部分工作都是在写templates
3. templates的放置：
    1. login.html等等在auth.urls.urlpatterns中提及的views对应的template都放在registration中
    2. base.html, home.html放在templates目录，而signup.html和之前的情况一样，也是放在templates目录中（不管有没有建立accounts app）

## urls

1. 在project级别的urlpatterns里面，users先指向自定义的users.urls，然后才是django自带的
2. users.urls所指向的是SignUpView

## views

1. SignUpView 继承 CreateView，作为注册这一用途，常规需要提供form_class, success_url以及template_name。
2. blogs app中也继承过 CreateView，但是当时是设置了model 和 fields

## forms

使用原先的UserCreationForm.Meta.fields + (...)的办法只能覆盖少数的几个field，包括username和password，但是我们还需要email，可能也需要first_name和last_name（这些可以在abstractUser的model定义里看到），所以直接使用一个tuple列举各个fieldname可能还更好

---

# bootstrap

## 前续工作收尾

1. 首先新建一个pages app替换掉之前home指向的TemplateView, project层面，修改settings和urls
2. 在pages app中建立urls， 修改views
3. test: django自带的功能是不需要测试的，自建的功能就需要测试。书中以template页面作为单位考虑测试，需要测试的页面包括home和signup两个页面
4. 从url出发, hard coded url和以name reverse得出的url两方面都要测试, template used也应该测试
    note: hard coded url末尾需要加上`/`, 否则肯定出错的
   
## Bootstrap

bootstrap建议使用cdn在线读取, 国内也有资源. 应该载入的资源包括:

• Bootstrap.css
• jQuery.js
• Popper.js
• Bootstrap.js 

主要的修改都集中在base.html里面. 添加了一个navbar. 接下来要对signup form作一些修正. 书里面使用的是第三方库 django-crispy-forms

使用步骤:

1. 安装django-crispy-forms (via. pip)
2. 在settings中将`'crispy_forms',`加入installed apps, 同时由于我们使用了bootstrap4而不是默认的bootstrap2, 需要添加`CRISPY_TEMPLATE_PACK = "bootstrap4"`
3. 在template文件中, 顶端加入:`{% load crispy_forms_tags %}`, 原先的`{{form.as_p}}`修正成`{{form|crispy}}`就可以了.

crispy form还有更丰富的功能, 不过目前暂时不作深入学习

---

# 密码修改与重设

这个是auth.urls的urlpatterns中剩下的几个东西. 实际上django已经有修改密码以及密码重设的模板了, 现在需要做的是自己建相应的模板. 这些模板文件都放在registration文件夹中

## 密码修改

password change, password change done这两个页面不需要做太多
    顺带一提，password_change不能直接通过users/password_change进入，因为这个是给已登录用户才开发的。

password reset这一块需要额外设置如何发送邮件. sendgrid是一个可行的工具，但是国内的适用性还有待论证。实际上sendcloud应该是更好用的，人家一天限量10封，基本上是应该够用的了（开发阶段）。生产阶段的话肯定就要花钱去订阅了……或者手工？毕竟大家都喜欢把密码设置成123456……

## 密码重置

重设这里，我发现走完步骤以后，点击登录的时候会报错，这是因为这时候系统会跳转到accounts/login，但是accouts这一系列的url在project级别没有注册过，所以要添加进来，当然可以继续用`django.contrib.auth.urls`来做

### 模板

- password_rest_form.html
- password_rest_done.html
- password_rest_confirm.html
- password_rest_complete.html

---

# email和sendcloud/sendgrid

关于邮件这一块先放一下, 等到网络环境较好的时候才开始做. 邮件这一章涉及了源码>>参考>>自建这样一个工作流程. 对于django这种非常庞大的项目, 通读全部代码是很困难的, 但是根据实际需求阅读相应的代码还是比较可行的

---

# app实际内容的编写

articles app 和之前的blogs相似。编写的过程肯定也是：

1. models
2. template， views， urls
    1. urls包括project level的include，以及app level的urlpatterns
    2. views 目前包括一个ListView
3. template中：
    1. object_list, 当然也可以通过context_object_name (views.py) 设置
    2. 用的是bootstrap的card这个对象。建议进一步阅读。
    3. 行内文本分区使用span
    4. 不同区域（题目，正文以及辅助区域）的分区使用的是div

另外，crispy forms如果只是用filter恐怕还是不能很好的排版，看来还是要学习form helper才行

## 添加edit，delete与list功能

1. urls：依靠`<int:pk>/.../`设置url。
2. views方面，注意ListView和DetailView来自 generic， 而DeleteView以及UpdateView来自 generic.edit。
    todo：能否从generic导入DeleteView与UpdateView: 经过测试, 直接从generic也是可以导入的, 所以到底有什么区别呢? 包括model的继承, 有人写models.Model, 但是models好像也可以?
3. 其实想一下, 各种view的写法真的差不多, 但是为什么可以实现各自的功能呢? 这不全靠着各种**generic view**么?

---

# 认证与鉴权

## create view 的修改

1. author应该是当前用户

在书中这个功能是借助form_valid()函数做的。但是具体原理书中语焉不详。这一块肯定要看一下django 文档中关于form的部分，另外最好也把crispy form一起看了。

2. 鉴权

class based views需要class mixin来提供鉴权功能

**LoginRequiredMixin** : 只有登录用户才能进入的view
**UserPassesTestMixin** : 对用户权限进一步细分. test指的是test_func, 需要手动override

```python
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
```

test_func中使用的get_object:

> get_object(queryset=None)
Returns **the single object that this view will display**. If queryset is provided, that queryset will be used as the source of objects; otherwise, get_queryset() will be used. get_object() looks for a pk_url_kwarg argument in the arguments to the view; if this argument is found, this method performs a primary-key based lookup using that value. If this argument is not found, it looks for a slug_url_kwarg argument, and performs a slug lookup using the slug_field.

> When query_pk_and_slug is True, get_object() will perform its lookup using both the primary key and the slug.

注意 **self.request**, 而且request里面还有user?

request.user除了可以在view里面使用, template里面也是可以的

至于书中说的编辑/删除在非当前用户写作文章记录里不予显示, 这个功能用不上custom template tag, 使用 {% if request.user == article.author %}就可以了. custom template tag确实有用, 但是不是用在这个功能上面

顺便说一下书里面也没有给article写test. 不过等我们跟着comment一章走完以后其实这一个学习project就算走完了, 接下来应该开始着手做会议系统了.

---

# comments

这里主要是一个inline form

虽然书中说新建一个app是over engineering, 不过我们还是尝试一下.

custom user那里的admin class:

```python
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username','age','is_staff','desc']

```
如果跟踪UserAdmin看过去可以发现, 这个class继承的是admin.ModelAdmin, 所以对于article和comment, 都可以自建一个admin class, 调节list_display, 而具体到编辑页面, 还能够添加inline编辑功能:

```python
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
```

注意上面实现步骤, 首先建立一个inline Class, 继承于admin的TabularInline/ StackedInline. 然后在ArticleAdmin里面的inlines field将其纳入

至于对inline class 的微调(额外显示的条目数), 自然是在inline class的内部

## template方面

这里第一次遇到反向查找. 之前我们是从一个object通过foreignkey找到它的宗主, 比如从article找到author. 但是现在我们是从article找到comments, article在这里是comment的宗主, 对于这种反向查找可以使用`query_set`

query_set在具体使用时是foo_set, 而foo则是对面model的名称的小写, 所以这里应该是comment_set. 和context_object_name一样, 这里也可以手动设置一个容易理解的名称作为query_set使用.

---

这个书的学习记录就到此为止了

