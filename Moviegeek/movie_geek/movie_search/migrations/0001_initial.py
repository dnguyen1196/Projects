# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('movie_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('c_action', models.IntegerField(null=True, db_column='C_action', blank=True)),
                ('c_adventure', models.IntegerField(null=True, db_column='C_adventure', blank=True)),
                ('c_animation', models.IntegerField(null=True, db_column='C_animation', blank=True)),
                ('c_children', models.IntegerField(null=True, db_column='C_children', blank=True)),
                ('c_comedy', models.IntegerField(null=True, db_column='C_comedy', blank=True)),
                ('c_crime', models.IntegerField(null=True, db_column='C_crime', blank=True)),
                ('c_documentary', models.IntegerField(null=True, db_column='C_documentary', blank=True)),
                ('c_drama', models.IntegerField(null=True, db_column='C_drama', blank=True)),
                ('c_fantasy', models.IntegerField(null=True, db_column='C_fantasy', blank=True)),
                ('c_film_noir', models.IntegerField(null=True, db_column='C_film_noir', blank=True)),
                ('c_horror', models.IntegerField(null=True, db_column='C_horror', blank=True)),
                ('c_musical', models.IntegerField(null=True, db_column='C_musical', blank=True)),
                ('c_mystery', models.IntegerField(null=True, db_column='C_mystery', blank=True)),
                ('c_romance', models.IntegerField(null=True, db_column='C_romance', blank=True)),
                ('c_sci_fi', models.IntegerField(null=True, db_column='C_sci_fi', blank=True)),
                ('c_thriller', models.IntegerField(null=True, db_column='C_thriller', blank=True)),
                ('c_war', models.IntegerField(null=True, db_column='C_war', blank=True)),
                ('c_western', models.IntegerField(null=True, db_column='C_western', blank=True)),
                ('rating', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'Movies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('timestamp', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'db_table': 'Ratings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(serialize=False, primary_key=True)),
                ('gender', models.CharField(max_length=1)),
                ('age', models.IntegerField()),
                ('occupation', models.IntegerField(null=True, blank=True)),
                ('zip', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': False,
            },
        ),
    ]
