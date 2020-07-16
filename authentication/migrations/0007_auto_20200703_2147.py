# Generated by Django 2.2.2 on 2020-07-03 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('school_email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('school_address', models.CharField(blank=True, max_length=255, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='School',
        ),
    ]