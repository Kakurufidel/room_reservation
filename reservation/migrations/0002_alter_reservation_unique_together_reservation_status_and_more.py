# Generated by Django 5.1.2 on 2024-10-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="reservation",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="reservation",
            name="status",
            field=models.CharField(default="pending", max_length=20),
        ),
        migrations.AddField(
            model_name="room",
            name="price",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
    ]