from django import forms
from django.contrib.auth.models import User
from .models import Club,Activity,message,InClub,Advertisement
from django.db import models

class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("name","club_id","Aboutme",)

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ("name","begin_date","end_date","description",)

class messageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ("content","receiver_name",)

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("name","club_id","Aboutme")

class CreateAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ("title","content","video","attach",)

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ("title","content","video","attach","show",)
