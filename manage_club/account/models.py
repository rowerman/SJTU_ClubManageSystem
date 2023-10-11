from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User,unique=True,related_name="user_info",on_delete=models.CASCADE)
    school = models.CharField(max_length=100,blank=True)            #学院
    department = models.CharField(max_length=100,blank=True)        #专业
    age = models.IntegerField(max_length=20,blank=True,default=18)                        #年龄
    level = models.CharField(max_length=20,blank=True)                         #年级
    phone = models.CharField(max_length=50,blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.TextField(max_length=500000,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user:{}".format(self.user.username)


