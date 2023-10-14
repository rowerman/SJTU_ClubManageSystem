from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .fields import OrderField

#社团信息
class Club(models.Model):
    leader = models.ForeignKey(User,related_name="leader",on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=100,unique=True)
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
    return "club/club_{0}/{1}".format(instance.owner.id,filename)

class Advertisement(models.Model):
    owner = models.ForeignKey(Club,related_name="advertisement",on_delete=models.CASCADE)
    show = models.CharField(max_length=10,default="on")
    content = models.TextField(max_length=1000,blank=True)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=user_directory_path,blank=True)
    attach = models.FileField(blank=True,upload_to=user_directory_path)
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True,for_fields=['owner'])

    class Meta:
        ordering = ['owner']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)




