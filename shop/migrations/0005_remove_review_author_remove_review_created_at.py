# Generated by Django 4.2.7 on 2023-12-10 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
    ]