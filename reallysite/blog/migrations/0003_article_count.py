# Generated by Django 4.1.5 on 2023-01-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="article", name="count", field=models.IntegerField(default=0),
        ),
    ]
