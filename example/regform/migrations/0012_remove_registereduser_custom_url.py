# Generated by Django 3.1.7 on 2021-08-16 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regform', '0011_auto_20210816_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registereduser',
            name='custom_url',
        ),
    ]
