# Generated by Django 4.2 on 2023-08-25 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0007_userprofile_blood_group_userprofile_contact_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
