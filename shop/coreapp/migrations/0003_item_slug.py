# Generated by Django 3.1.13 on 2021-08-14 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_auto_20210814_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
