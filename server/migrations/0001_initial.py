# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'alist',
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('app_id', models.CharField(max_length=100, unique=True)),
                ('app_name', models.CharField(max_length=100)),
                ('app_token', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'apps',
            },
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unique_name', models.CharField(max_length=50, unique=True)),
                ('confer_name', models.CharField(max_length=50, unique=True)),
                ('title', models.TextField()),
                ('subtitle', models.TextField()),
                ('blurb', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('hidden', models.BooleanField(default=False)),
                ('admins', models.TextField(default=b'[]')),
            ],
            options={
                'ordering': ['-start_date'],
                'db_table': 'conferences',
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('paper_id', models.TextField()),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Conference')),
            ],
            options={
                'db_table': 'following',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('likes', models.TextField()),
            ],
            options={
                'db_table': 'likes',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=50)),
                ('data', models.TextField()),
            ],
            options={
                'ordering': ['-timestamp'],
                'db_table': 'logs',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('access', models.BooleanField(default=False)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.App')),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('voter_id', models.CharField(max_length=20, null=True, unique=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Conference')),
            ],
            options={
                'db_table': 'registrations',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('meetups_enabled', models.BooleanField(default=False)),
                ('friendly', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.User'),
        ),
        migrations.AddField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.User'),
        ),
        migrations.AddField(
            model_name='logs',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Registration'),
        ),
        migrations.AddField(
            model_name='likes',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Registration'),
        ),
        migrations.AddField(
            model_name='following',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.User'),
        ),
        migrations.AddField(
            model_name='app',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.User'),
        ),
        migrations.AddField(
            model_name='alist',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Registration'),
        ),
        migrations.AddField(
            model_name='alist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='server.User'),
        ),
        migrations.AddField(
            model_name='alist',
            name='user_starred',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_starred', to='server.User'),
        ),
        migrations.AlterUniqueTogether(
            name='following',
            unique_together=set([('paper_id', 'conference', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='alist',
            unique_together=set([('registration', 'user', 'user_starred')]),
        ),
    ]
