# Generated by Django 2.2.2 on 2020-08-31 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20200829_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='counter',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
