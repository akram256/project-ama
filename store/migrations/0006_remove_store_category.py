# Generated by Django 2.2.2 on 2020-08-22 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200822_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='category',
        ),
    ]
