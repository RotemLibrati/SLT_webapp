# Generated by Django 3.0.2 on 2020-01-13 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
