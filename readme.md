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
