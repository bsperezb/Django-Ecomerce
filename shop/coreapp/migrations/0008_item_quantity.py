# Generated by Django 3.1.13 on 2021-08-16 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0007_auto_20210816_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
