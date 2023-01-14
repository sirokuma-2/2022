# Generated by Django 4.1.5 on 2023-01-12 20:04

from django.db import migrations, models
import mysite.models.profile_models


class Migration(migrations.Migration):

    dependencies = [
        ("mysite", "0002_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to=mysite.models.profile_models.upload_image_to,
            ),
        ),
    ]