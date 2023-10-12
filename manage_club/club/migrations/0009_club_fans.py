# Generated by Django 4.2.5 on 2023-10-11 00:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("club", "0008_alter_userlevel_club"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="fans",
            field=models.ManyToManyField(
                blank=True, related_name="fans", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
