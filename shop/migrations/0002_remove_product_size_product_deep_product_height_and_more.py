# Generated by Django 4.2.7 on 2023-12-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='deep',
            field=models.IntegerField(default=30, verbose_name='Глубина'),
        ),
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.IntegerField(default=30, verbose_name='Высота'),
        ),
        migrations.AddField(
            model_name='product',
            name='weigh',
            field=models.IntegerField(default=30, verbose_name='Ширина'),
        ),
    ]
