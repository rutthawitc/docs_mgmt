# Generated by Django 3.0.6 on 2020-05-25 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsmgmt', '0012_auto_20200525_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
