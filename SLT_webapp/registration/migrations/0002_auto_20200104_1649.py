# Generated by Django 3.0.1 on 2020-01-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(auto_created=0),
        ),
    ]
