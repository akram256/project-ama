# Generated by Django 2.2.2 on 2020-09-26 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_totalamount_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TotalAmount',
        ),
    ]