# Generated by Django 4.2.5 on 2023-10-14 07:18

import club.fields
import club.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0014_club_leader"),
    ]

    operations = [
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("show", models.CharField(default="on", max_length=10)),
                ("content", models.TextField(blank=True, max_length=1000)),
                ("title", models.CharField(max_length=100)),
                ("video", models.FileField(upload_to=club.models.user_directory_path)),
                (
                    "attach",
                    models.FileField(
                        blank=True, upload_to=club.models.user_directory_path
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("order", club.fields.OrderField(blank=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="advertisement",
                        to="club.club",
                    ),
                ),
            ],
            options={
                "ordering": ["owner"],
            },
        ),
    ]
