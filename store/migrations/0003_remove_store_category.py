# Generated by Django 2.2.2 on 2020-08-22 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='category',
        ),
    ]