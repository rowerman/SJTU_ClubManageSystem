from django.contrib.auth.models import User
from django.db import models


#社团信息
class Club(models.Model):
    name = models.CharField(max_length=100,unique=True)
    lead_name = models.CharField(max_length=100,default="hanwen")
    club_id = models.CharField(max_length=100)          #社团编号
    created = models.DateTimeField(auto_now_add=True)
    num_of_mem = models.IntegerField(max_length=500,default=1)
    photo = models.TextField(max_length=10000,blank=True)
    Aboutme = models.TextField(max_length=1000)

class InClub(models.Model):
    member = models.OneToOneField(User,related_name="member",on_delete=models.CASCADE)
    In_club = models.ManyToManyField(Club,related_name="In_club")

class Activity(models.Model):
    name = models.CharField(max_length=100,unique=True)
    begin_date = models.DateTimeField(max_length=100)
    end_date = models.DateTimeField(max_length=100)
    description = models.TextField(max_length=1000)
    belong = models.ForeignKey(Club,related_name="launch",on_delete=models.CASCADE)

class message(models.Model):
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    reciver = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=100,default="hanwen")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver_read = models.BooleanField(default=False)

class UserLevel(models.Model):
    user = models.OneToOneField(User,unique=True,related_name="user_level",on_delete=models.CASCADE)
    #1.普通成员：common_member  2.管理员：manager  3.社长：leader
    level = models.CharField(max_length=100,default="common_member")
    club = models.ForeignKey(Club,related_name="club_level",on_delete=models.CASCADE)



