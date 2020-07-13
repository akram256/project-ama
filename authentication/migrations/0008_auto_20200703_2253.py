# Generated by Django 2.2.2 on 2020-07-03 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20200703_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('SCHOOL', 'SCHOOL'), ('USER', 'USER')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='school_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='school_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='SchoolUser',
        ),
    ]
