# Generated by Django 2.2.2 on 2020-07-24 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_auto_20200717_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
    ]
