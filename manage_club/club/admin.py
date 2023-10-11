from django.forms import TextInput, Textarea
from django.db import models
from django.contrib import admin
from .models import Club,Activity,InClub,UserLevel
# Register your models here.

class ClubAdmin(admin.ModelAdmin):
    list_display = ("name","club_id","num_of_mem","Aboutme","created")
    list_filter = ("club_id","num_of_mem","created")

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
admin.site.register(Club,ClubAdmin)

class ActivityAdmin(admin.ModelAdmin):
    def post_activity(self, obj):
        return [pt.name for pt in obj.belong.all()]
    list_display = ("name","begin_date","end_date","description","post_activity")
    list_filter = ("begin_date","name")

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
admin.site.register(Activity,ActivityAdmin)

class UserLevelAdmin(admin.ModelAdmin):
    def get_club_name(self, obj):
        return obj.club.name
    def get_user_name(self,obj):
        return obj.user.username
    get_club_name.short_description = "Club name"
    get_user_name.short_description = "Menber name"
    list_display = ("get_user_name","level","get_club_name",)
    list_filter = ("level","club",)

admin.site.register(UserLevel,UserLevelAdmin)

