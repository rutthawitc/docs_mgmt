# Generated by Django 3.0.6 on 2020-05-25 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docsmgmt', '0013_documents_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='doc_dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.UserDepartment'),
        ),
    ]
