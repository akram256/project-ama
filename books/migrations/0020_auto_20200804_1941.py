# Generated by Django 2.2.2 on 2020-08-04 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_bookmodel_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='book_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookClass'),
        ),
    ]
