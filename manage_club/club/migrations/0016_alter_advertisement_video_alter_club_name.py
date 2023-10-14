# Generated by Django 4.2.5 on 2023-10-14 10:38

import club.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0015_advertisement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="video",
            field=models.FileField(
                blank=True, upload_to=club.models.user_directory_path
            ),
        ),
        migrations.AlterField(
            model_name="club",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]