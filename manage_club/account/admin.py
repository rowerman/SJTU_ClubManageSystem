from django.contrib import admin
from .models import UserInfo
from django.forms import TextInput, Textarea
from django.db import models


# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user",'school','age','level','aboutme','photo','phone','created','department')
    list_filter = ("school","department","level")
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
admin.site.register(UserInfo,UserInfoAdmin)

