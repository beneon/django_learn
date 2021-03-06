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

