# Generated by Django 2.2.2 on 2020-07-13 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_age_category_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='age_category',
            name='pic',
        ),
    ]
