# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class History(models.Model):
    datetime = models.IntegerField()
    station_type = models.CharField(max_length=64)
    active = models.IntegerField()
    stale = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history'
        app_label = 'old_db'


class PlatformHistory(models.Model):
    datetime = models.IntegerField()
    platform_info = models.CharField(max_length=256)
    active = models.IntegerField()
    stale = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'platform_history'
        app_label = 'old_db'


class PythonHistory(models.Model):
    datetime = models.IntegerField()
    python_info = models.CharField(max_length=256)
    active = models.IntegerField()
    stale = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'python_history'
        app_label = 'old_db'


class OldStations(models.Model):
    station_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, default=None)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)
    station_type = models.CharField(max_length=64, null=True, default=None)
    station_model = models.CharField(max_length=128, null=True, default=None)
    weewx_info = models.CharField(max_length=64, null=True, default=None)
    python_info = models.CharField(max_length=64, null=True, default=None)
    platform_info = models.CharField(max_length=128, null=True, default=None)
    last_addr = models.CharField(max_length=16, null=True, default=None)
    last_seen = models.IntegerField(null=True, default=None)

    class Meta:
        managed = False
        db_table = 'stations'
        app_label = 'old_db'


class WeeWXHistory(models.Model):
    datetime = models.IntegerField()
    weewx_info = models.CharField(max_length=256)
    active = models.IntegerField()
    stale = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'weewx_history'
        app_label = 'old_db'
