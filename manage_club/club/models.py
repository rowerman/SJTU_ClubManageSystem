from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .fields import OrderField
import os

#社团信息
class Club(models.Model):
    leader = models.ForeignKey(User,related_name="leader",on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=100)
    lead_name = models.CharField(max_length=100,default="hanwen")
    club_id = models.CharField(max_length=100)          #社团宣言
    created = models.DateTimeField(auto_now_add=True)
    num_of_mem = models.IntegerField(max_length=500,default=1)
    photo = models.TextField(max_length=10000,blank=True)
    Aboutme = models.TextField(max_length=1000)
    fans = models.ManyToManyField(User,related_name="fans",blank=True)

class InClub(models.Model):
    member = models.OneToOneField(User,related_name="member",on_delete=models.CASCADE)
    In_club = models.ManyToManyField(Club,related_name="In_club")

class Activity(models.Model):
    name = models.CharField(max_length=100,unique=True)
    begin_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000)
    belong = models.ForeignKey(Club,related_name="launch",on_delete=models.CASCADE)

class message(models.Model):
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    reciver = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=100,default="hanwen")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver_read = models.CharField(max_length=10,default="no")

def user_directory_path(instance,filename):
    return "club/club_{0}/{1}".format(instance.owner.name,filename)

def delete_directory(path):
    if os.path.exists(path):
        # 确保目录为空
        if not os.listdir(path):
            # 删除目录
            os.rmdir(path)
            return True
        else:
            print("目录不为空，无法删除！")
    else:
        print("目录不存在！")
    return False

class Advertisement(models.Model):
    owner = models.ForeignKey(Club,related_name="advertisement",on_delete=models.CASCADE)
    show = models.CharField(max_length=10,default="on")
    content = models.TextField(max_length=1000,blank=True)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=user_directory_path,blank=True)
    attach = models.FileField(blank=True,upload_to=user_directory_path)
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True,for_fields=['owner'])

    def delete(self, *args, **kwargs):
        # 删除视频文件
        if self.video:
            # 获取视频文件的路径
            video_path = os.path.join('images', str(self.video))
            # 删除视频文件
            if os.path.exists(video_path):
                os.remove(video_path)
            parent_directory = os.path.dirname(video_path)  # 获取上一级目录
            delete_directory(parent_directory)

        # 删除附件文件
        if self.attach:
            # 获取附件文件的路径
            attach_path = os.path.join('images', str(self.attach))
            # 删除附件文件
            if os.path.exists(attach_path):
                os.remove(attach_path)
            parent_directory = os.path.dirname(attach_path)  # 获取上一级目录
            delete_directory(parent_directory)

        # 调用父类的 delete() 方法删除数据库信息
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['owner']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)




