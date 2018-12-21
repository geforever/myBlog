"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from Blog.settings import MEDIA_ROOT
import login.views as view
import personal_blog.views as blog_view
import BBS.views as BBS_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index),
    url(r'^index/', view.index),
    url(r'^login/', view.login),
    url(r'^register/', view.register),
    url(r'^logout/', view.logout),
    url(r'^blog/$', blog_view.blog),
    url(r'^captcha', include('captcha.urls')),
    url(r'^my_blog/$', blog_view.my_blog),
    url(r'^bbs/', BBS_view.bbs_index),
    url(r'^my_blog/add_blog/$', blog_view.add_blog),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('blog/article_detail/<int:id>/', blog_view.article_detail, name='article_detail'),
]
