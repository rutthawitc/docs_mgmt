# Generated by Django 3.0.6 on 2020-05-19 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docsmgmt', '0007_auto_20200519_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='upload_by',
        ),
    ]