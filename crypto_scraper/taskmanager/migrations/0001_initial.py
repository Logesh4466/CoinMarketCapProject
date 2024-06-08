# Generated by Django 5.0.6 on 2024-06-07 12:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('coin', models.CharField(max_length=50)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('result', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]