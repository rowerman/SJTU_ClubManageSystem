from django.db import models
from club.models import Club

class GoodType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

class Commodity(models.Model):
    name = models.CharField(max_length=50,help_text="不超过50个字符")
    status = models.CharField(max_length=10,default="selling")              #两种类型：selling和sold
    contact = models.CharField(max_length=100)
    expense = models.FloatField()
    intro = models.TextField(max_length=500,help_text="不超过500个字符")
    owner = models.ForeignKey(Club,related_name="owner",on_delete=models.CASCADE)
    Type = models.ManyToManyField(GoodType,related_name="Type",blank=True)
