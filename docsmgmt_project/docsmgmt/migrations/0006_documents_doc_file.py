# Generated by Django 3.0.6 on 2020-05-18 12:41

from django.db import migrations, models
import docsmgmt.models


class Migration(migrations.Migration):

    dependencies = [
        ('docsmgmt', '0005_auto_20200517_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='doc_file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=docsmgmt.models.path_and_rename),
        ),
    ]
