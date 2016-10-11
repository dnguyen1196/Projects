# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    c_action = models.IntegerField(db_column='C_action', blank=True, null=True)  # Field name made lowercase.
    c_adventure = models.IntegerField(db_column='C_adventure', blank=True, null=True)  # Field name made lowercase.
    c_animation = models.IntegerField(db_column='C_animation', blank=True, null=True)  # Field name made lowercase.
    c_children = models.IntegerField(db_column='C_children', blank=True, null=True)  # Field name made lowercase.
    c_comedy = models.IntegerField(db_column='C_comedy', blank=True, null=True)  # Field name made lowercase.
    c_crime = models.IntegerField(db_column='C_crime', blank=True, null=True)  # Field name made lowercase.
    c_documentary = models.IntegerField(db_column='C_documentary', blank=True, null=True)  # Field name made lowercase.
    c_drama = models.IntegerField(db_column='C_drama', blank=True, null=True)  # Field name made lowercase.
    c_fantasy = models.IntegerField(db_column='C_fantasy', blank=True, null=True)  # Field name made lowercase.
    c_film_noir = models.IntegerField(db_column='C_film_noir', blank=True, null=True)  # Field name made lowercase.
    c_horror = models.IntegerField(db_column='C_horror', blank=True, null=True)  # Field name made lowercase.
    c_musical = models.IntegerField(db_column='C_musical', blank=True, null=True)  # Field name made lowercase.
    c_mystery = models.IntegerField(db_column='C_mystery', blank=True, null=True)  # Field name made lowercase.
    c_romance = models.IntegerField(db_column='C_romance', blank=True, null=True)  # Field name made lowercase.
    c_sci_fi = models.IntegerField(db_column='C_sci_fi', blank=True, null=True)  # Field name made lowercase.
    c_thriller = models.IntegerField(db_column='C_thriller', blank=True, null=True)  # Field name made lowercase.
    c_war = models.IntegerField(db_column='C_war', blank=True, null=True)  # Field name made lowercase.
    c_western = models.IntegerField(db_column='C_western', blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Movies'

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    occupation = models.IntegerField(blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'

class Ratings(models.Model):
    user = models.ForeignKey('Users')
    movie = models.ForeignKey(Movies)
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ratings'



