# Generated by Django 3.1.7 on 2021-08-22 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regform', '0015_auto_20210823_0203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpost',
            options={'ordering': ['-datetime'], 'verbose_name': 'Пост пользователя', 'verbose_name_plural': 'Посты пользователя'},
        ),
    ]
