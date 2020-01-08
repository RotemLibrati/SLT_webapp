# Generated by Django 3.0.1 on 2020-01-08 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='difficulty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='number_of_mistakes',
            field=models.IntegerField(default=0),
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
    ]
