# Generated by Django 3.2.20 on 2023-07-15 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_customuser_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='following',
        ),
    ]
