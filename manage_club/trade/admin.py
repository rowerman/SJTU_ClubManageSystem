from django.contrib import admin
from .models import GoodType

# Register your models here.
class GoodTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    list_filter = ("type",)

admin.site.register(GoodType,GoodTypeAdmin)

