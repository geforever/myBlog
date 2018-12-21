from django.shortcuts import render,HttpResponse,redirect
from personal_blog.models import Blog
from login.models import User
import datetime
import os


# Create your views here.



def blog(request):
    a = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': a})


def my_blog(request):
    user_name = request.session.get('user_name')
    user = User.objects.get(user_name=user_name)
    my_blog = Blog.objects.filter(author_id=user.id)
    if my_blog:
        return render(request, 'my_blog.html', {'my_blogs': my_blog})
    return render(request, 'my_blog.html')

def add_blog(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            message = "请检查填写内容"
            title = request.POST['title']
            body = request.POST['body']
            if title:
                if body:
                    try:
                        user_name = request.session.get('user_name')
                        author = User.objects.get(user_name=user_name)
                        if request.FILES.get('video'):
                            try:
                                video_file = request.FILES.get('video')
                                video_name = request.FILES.get('video').name
                                if str(os.path.splitext(video_name)[1]).lower() != '.mp4':
                                    message = "该文件不是MP4格式，请重新选择！"
                                    return render(request, 'add_blog.html', locals())
                                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取当前时间
                                video_name = request.session.get('user_name') + "-" \
                                             + str(request.session.get('user_id')) + str(now_time) + "-" + video_name
                                file_path = os.path.join('media', 'upload', video_name)
                                f = open(file_path, 'wb')
                                for chunk in video_file.chunks():#储存视频
                                    f.write(chunk)
                                f.close()
                            except:
                                message = "文件上传有误"
                                return render(request, 'add_blog.html', locals())
                        else:
                            video_name = None

                        new_blog = Blog.objects.create(
                            blog_title=title, blog_body=body, author_id=author.id, blog_videoname=video_name
                        )
                        new_blog.save()
                        return redirect('/my_blog/')
                    except:
                        message = "无此用户"
                        return render(request, 'add_blog.html', locals())
                else:
                    message = "内容不能为空"
                    return render(request, 'add_blog.html', locals())
            else:
                message = "标题不能为空"
                return render(request, 'add_blog.html', locals())
    return render(request, 'add_blog.html', locals())



def article_detail(request, id):
    id = int(id)
    article_detail = Blog.objects.get(id=id)
    return render(request, 'detail.html', {'article_detail': article_detail})