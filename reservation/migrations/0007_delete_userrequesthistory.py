# Generated by Django 4.2.16 on 2024-11-05 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0006_userrequesthistory"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserRequestHistory",
        ),
    ]
