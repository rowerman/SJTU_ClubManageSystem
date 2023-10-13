from django.forms import TextInput, Textarea
from django.db import models
from django.contrib import admin
from .models import Club,Activity,InClub
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


