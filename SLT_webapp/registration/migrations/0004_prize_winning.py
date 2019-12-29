# Generated by Django 3.0.1 on 2019-12-29 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20191229_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=200)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Winning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_date', models.DateTimeField(auto_now_add=True)),
                ('prize', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Prize')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.User')),
            ],
        ),
    ]
