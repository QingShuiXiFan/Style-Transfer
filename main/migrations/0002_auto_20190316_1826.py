# Generated by Django 2.1.7 on 2019-03-16 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='c_time',
        ),
    ]
