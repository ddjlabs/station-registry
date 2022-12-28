from django.contrib import admin
from . models import MetricMappings, GeographyMappings


# Register your models here.
admin.site.register(MetricMappings)
admin.site.register(GeographyMappings)
