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



