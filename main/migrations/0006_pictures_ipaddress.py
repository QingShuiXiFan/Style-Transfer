# Generated by Django 2.1.7 on 2019-04-01 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190331_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictures',
            name='ipAddress',
            field=models.GenericIPAddressField(default='0.0.0.0', protocol='ipv4'),
        ),
    ]
