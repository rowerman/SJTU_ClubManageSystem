# Generated by Django 4.2.5 on 2023-10-12 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0012_alter_message_receiver_read"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="begin_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="activity",
            name="end_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]