from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from login.models import User
from login.forms import UserForm
from login.forms import RegisterForm

# Create your views here.


def index(request):
    pass
    return render(request, 'index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(user_name=username)
                if password == user.password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.user_name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())#{"message": message}

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次输入的密码不相同"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(user_name=username)
                if same_name_user:
                    message = "用户已经存在，请重新输入"
                    return render(request, 'register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = "该邮箱已经被注册，请使用其他邮箱"
                    return render(request, 'register.html', locals())

                new_user = User.objects.create()
                new_user.user_name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    #request.session.flush()
    # 或者使用下面的方法
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return redirect("/index/")


