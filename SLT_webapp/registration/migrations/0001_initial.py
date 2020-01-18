# Generated by Django 3.0.1 on 2020-01-18 18:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=256)),
                ('receiver', models.CharField(max_length=256)),
                ('msg', models.TextField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('condition_type', models.CharField(choices=[('time', 'time'), ('moves', 'moves'), ('mistakes', 'mistakes')], default='time', max_length=20)),
                ('condition', models.IntegerField(default=1000)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('parent', 'parent'), ('student', 'student')], default='student', max_length=10)),
                ('is_admin', models.BooleanField(default=False)),
                ('suspention_time', models.DateTimeField(default=datetime.datetime(2020, 1, 18, 18, 55, 19, 130890, tzinfo=utc))),
                ('total_minutes', models.FloatField(default=0)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('rank', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('son', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='son', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=256)),
                ('last_visit', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Winning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_date', models.DateTimeField(default=datetime.datetime(2020, 1, 18, 18, 55, 19, 133890, tzinfo=utc))),
                ('seen', models.BooleanField(default=False)),
                ('prize', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Prize')),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserReoprt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=100)),
                ('reported', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=256)),
                ('seen', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('body', models.CharField(blank=True, max_length=250)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_by_sender', models.BooleanField(default=False)),
                ('deleted_by_receiver', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_mistakes', models.IntegerField(default=0)),
                ('number_of_moves', models.IntegerField(default=0)),
                ('time_start', models.DateTimeField(default=datetime.datetime(2020, 1, 18, 18, 55, 19, 134890, tzinfo=utc))),
                ('time_stop', models.DateTimeField(blank=True, null=True)),
                ('difficulty', models.IntegerField(default=0)),
                ('finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='uploads/')),
                ('authorized', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
