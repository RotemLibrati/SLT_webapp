# Generated by Django 3.0.1 on 2020-01-15 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20200115_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='suspention_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 15, 12, 9, 19, 726243)),
        ),
    ]
