# Generated by Django 2.2.2 on 2020-08-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_new_user',
            field=models.BooleanField(default=False),
        ),
    ]
