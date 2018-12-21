from django.db import models
from django.utils import timezone
from login.models import User

# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=256, null=False)
    blog_body = models.TextField()
    blog_create_time = models.DateTimeField(default=timezone.now())
    blog_update_time = models.DateTimeField(auto_now=True)
    blog_videoname = models.CharField(max_length=256,null=True)

    def __str__(self):
        return self.blog_title

    class Meta:
        ordering = ('-blog_create_time', )


