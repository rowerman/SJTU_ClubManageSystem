# Generated by Django 4.2.5 on 2023-10-11 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("club", "0010_remove_userlevel_club_userlevel_club"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoodType",
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
                ("type", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Commodity",
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
                ("name", models.CharField(help_text="不超过50个字符", max_length=50)),
                ("status", models.CharField(default="selling", max_length=10)),
                ("contact", models.CharField(max_length=100)),
                ("expense", models.FloatField()),
                ("intro", models.TextField(help_text="不超过500个字符", max_length=500)),
                (
                    "Type",
                    models.ManyToManyField(
                        blank=True, related_name="Type", to="trade.goodtype"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to="club.club",
                    ),
                ),
            ],
        ),
    ]
