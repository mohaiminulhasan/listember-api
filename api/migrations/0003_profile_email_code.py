# Generated by Django 3.2.5 on 2021-07-19 04:27

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_profile_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_code',
            field=models.CharField(default=api.utils.random_string, max_length=5),
        ),
    ]
