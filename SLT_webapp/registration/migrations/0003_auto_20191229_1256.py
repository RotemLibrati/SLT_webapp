# Generated by Django 3.0.1 on 2019-12-29 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20191229_0213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='user_friend',
            new_name='users',
        ),
        migrations.AddField(
            model_name='friend',
            name='current_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='registration.User'),
        ),
    ]