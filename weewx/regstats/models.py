from django.db import models
from stationregistry.models import StationStatus
from django.utils.timezone import now

# ===== Station Statistics Data Cube Tables START =====
class MetricTypes(models.Model):
    metric_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    lst_updt_ts = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f'{self.metric_type_id}, {self.name}'


class Metrics(models.Model):
    metric_id = models.AutoField(primary_key=True)
    metric_type = models.ForeignKey(MetricTypes, on_delete=models.DO_NOTHING, db_index=True, help_text="Metric Type")
    name = models.CharField(max_length=200, null=False, db_index=True)
    attrib1 = models.CharField(max_length=100, db_index=True, null=True)
    attrib2 = models.CharField(max_length=100, db_index=True, null=True)
    attrib3 = models.CharField(max_length=100, db_index=True, null=True)
    attrib4 = models.CharField(max_length=100, db_index=True, null=True)
    attrib5 = models.CharField(max_length=100, db_index=True, null=True)
    lst_updt_ts = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f'{self.name}, {self.metric_type}, {self.attrib1}, {self.attrib2}, {self.attrib3}, {self.attrib4}, {self.attrib5}'

class MetricMappings(models.Model):
    metric_mapping_id = models.AutoField(primary_key=True)
    metric_type = models.ForeignKey(MetricTypes, on_delete=models.DO_NOTHING, db_index=True, help_text="Metric Type")
    source_val = models.CharField(max_length=200, null=False, db_index=True, help_text="Station Entry Source Value")
    target_val = models.CharField(max_length=200, null=False, help_text="Target Metric Name")
    metric = models.ForeignKey(Metrics, on_delete=models.DO_NOTHING, db_index=True, help_text="Assigned Metric")
    lst_updt_ts = models.DateTimeField(default=now, blank=True)
    
    def __str__(self):
        return f'{self.metric_type}, {self.source_val}, {self.target_val}, {self.metric}, {self.lst_updt_ts}'


class StationStats(models.Model):
    stat_id = models.AutoField(primary_key=True)
    report_dt = models.DateField(null=False, db_index=True)
    metric = models.ForeignKey(Metrics, on_delete=models.CASCADE, db_index=True)
    station_status = models.ForeignKey(StationStatus, on_delete=models.DO_NOTHING, db_index=True)
    data_val = models.FloatField(null=False)


    def __str__(self):
        return f'{self.report_dt}, {self.metric}, {self.station_status}, {self.data_val}'



# ===== WeeWX Geographical Demographics tables =====

class Geography(models.Model):
    geo_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=3, null=False, default=None, db_index=True)
    province = models.CharField(max_length=100,null=True,default='unknown', db_index=True)
    city = models.CharField(max_length=100, null=True, default='unknown', db_index=True)
    lst_updt_ts = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f'{self.country_code}, {self.province}, {self.city}'

class GeographyMappings(models.Model):
    geo_map_id = models.AutoField(primary_key=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, default=None, blank=True, help_text="latitude value provided by the weather station client")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=None, blank=True)
    source_country_code = models.CharField(max_length=3, null=False, db_index=True)
    source_province = models.CharField(max_length=100, null=False, db_index=True)
    source_city = models.CharField(max_length=100, null=False, db_index=True)
    target_country_code = models.CharField(max_length=3, null=True, blank=True)
    target_province = models.CharField(max_length=100, null=True, blank=True)
    target_city = models.CharField(max_length=100, null=True, blank=True)
    geo = models.ForeignKey(Geography, on_delete=models.DO_NOTHING, db_index=True)
    lst_updt_ts = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f'{self.source_country_code}, {self.source_provincee}, {self.source_city}, {self.geo}'

    def lookup_mapping(self, lat : int, long : int, country_code : str, province : str, city : str):
        try:
            o_result = self.objects.filter(latitude__iexact=lat, longitude__iexact=long, source_country_code__iexact=country_code, source_province__iexact=province, source_city__iexact=city)
            return o_result
        except Exception as err:
            raise err

class GeoStats(models.Model):
    geo_stat_id = models.AutoField(primary_key=True)
    report_dt = models.DateField(null=False, editable=False, db_index=True)
    geo = models.ForeignKey(Geography, on_delete=models.DO_NOTHING, db_index=True)
    station_status = models.ForeignKey(StationStatus, on_delete=models.DO_NOTHING, db_index=True)
    data_val = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.geo}, {self.station_status}, {self.data_val}'
