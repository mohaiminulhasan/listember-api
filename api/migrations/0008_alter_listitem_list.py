# Generated by Django 3.2.5 on 2021-08-08 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_list_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.list'),
        ),
    ]
