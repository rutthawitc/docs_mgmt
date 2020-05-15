# Generated by Django 3.0.6 on 2020-05-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsmgmt', '0002_auto_20200515_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='doc_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='doc_mtno',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='documentsections',
            name='section_desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='refdocumenttype',
            name='type_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userdepartment',
            name='department_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='usersection',
            name='section_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]