# Generated by Django 4.2.5 on 2023-10-08 00:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0004_message_reciver_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="reciver_name",
            new_name="receiver_name",
        ),
    ]
