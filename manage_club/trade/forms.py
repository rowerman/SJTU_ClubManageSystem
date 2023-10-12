from django import forms
from django.contrib.auth.models import User
from .models import GoodType,Commodity

class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ("name","expense","intro","Type","contact",)