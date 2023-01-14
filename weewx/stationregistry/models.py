from django.db import models
from django.utils import timezone


# ===== REFERENCE TABLES START =====
class StationStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    lst_updt_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}, {self.name}'


# ===== Base Tables START =====
class Stations(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_url = models.URLField(null=False, unique=True, db_index=True, max_length=250,
                                  help_text="url provided by the weather station client upon registration")
    valid_url_yn = models.BooleanField(default=False,
                                       help_text="Flag that indicates the URL provided is active (returns 200 response)")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False,
                                   help_text="latitude value provided by the weather station client")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=False,
                                    help_text="longitude value provided by the weather station client")
    location_city = models.CharField(max_length=100, null=True, default=None)
    location_province = models.CharField(max_length=100, null=True, default=None)
    location_country_code = models.CharField(max_length=3, null=True, default=None)
    description = models.CharField(max_length=255, null=True)
    station_type = models.CharField(max_length=100)
    station_model = models.CharField(max_length=150)
    weewx_info = models.CharField(max_length=64)
    python_info = models.CharField(max_length=64)
    platform_info = models.CharField(max_length=150)
    config_path = models.CharField(max_length=255, null=True, default=None)
    entry_path = models.CharField(max_length=255, null=True, default=None)
    last_ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)
    register_dt = models.DateTimeField(default=timezone.now,
                                       help_text='Date when the station registry record was first created.')
    last_entry_dt = models.DateTimeField(null=False, help_text='Last entry datetime stamp.')
    last_url_check_dt = models.DateTimeField(null=True,
                                             help_text='Last time the URL was checked to see if it was still active.')
    site_profile_image_gen_dt = models.DateTimeField(null=True, default=None,
                                                     help_text='Last timestamp of when the stations profile image was created.')
    station_status_id = models.IntegerField(default=1, null=False)
    station_site_image = models.CharField(max_length=100, null=True, default=None, help_text='Thumbnail of the Weather Stations home page.')


    def __str__(self):
        return f'{self.station_id}, {self.station_url}, {self.latitude}, {self.longitude}, {self.description}'





class StationEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    entry_dt = models.DateTimeField(default=timezone.now, db_index=True)
    station = models.ForeignKey(Stations, on_delete=models.DO_NOTHING, db_index=True,
                                 help_text="Station ID from the Stations Table.")
    station_url = models.URLField(null=False, db_index=True, max_length=250,
                                  help_text="url provided by the weather station client upon registration")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False,
                                   help_text="latitude value provided by the weather station client")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=False)
    description = models.CharField(max_length=255, null=True)
    station_type = models.CharField(max_length=100)
    station_model = models.CharField(max_length=150)
    weewx_info = models.CharField(max_length=64)
    python_info = models.CharField(max_length=64)
    platform_info = models.CharField(max_length=150)
    config_path = models.CharField(max_length=255, null=True, default=None)
    entry_path = models.CharField(max_length=255, null=True, default=None)    
    last_ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)

    def __str__(self):
        return f'{self.stations}, {self.station_url}, {self.latitude}, {self.longitude}, {self.description}'




class URLBlackList(models.Model):
    url_blacklist_id = models.AutoField(primary_key=True)
    url_name = models.URLField(max_length=50, null=False, unique=True, db_index=True,
                               help_text="Domain/base URL that we are going to blacklist")
    url_reason = models.CharField(max_length=100)
    lst_updt_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.url_name}'
