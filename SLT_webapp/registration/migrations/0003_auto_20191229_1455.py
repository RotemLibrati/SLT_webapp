# Generated by Django 3.0.1 on 2019-12-29 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20191229_0213'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_mistakes', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('difficulty', models.IntegerField()),
                ('time_signature', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
    ]
