import logging
import datetime
from django.db import connection
from datetime import date
from .models import GeographyMappings, Geography, Metrics, MetricMappings, MetricTypes


logger = logging.getLogger(__name__)


def load_station_type_metrics():
    try:

        i_metric_type_id = 2  # Station Type is Metric Type 2

        with connection.cursor() as c:
            c.execute("""select distinct station_type from stationregistry_stationentry
                        where length(station_type) > 0 
                        and station_type not in (select distinct source_val from regstats_metricmappings rm where rm.metric_type_id =2)
                        """)
            rows = c.fetchall()

        logger.warn('Loading Station Type Metadata to Metrics Table (Including mappings)')

        for rec in rows:
            o_metrics = Metrics.objects.filter(name__iexact=rec[0])

            if o_metrics.exists():
                #Get the first record as there should only be 1 distict station type from the list
                o_rec = o_metrics[0]

                #Get the metric name from the station type
                s_metric_name = o_rec.name
                i_metric_id = o_rec.metric_id

                #Check the mapping table for a record
                o_metric_map = MetricMappings.objects.filter(metric_type_id=i_metric_type_id, source_val__iexact=s_metric_name)

                #Check if we DO NOT have a mapping. if this is true, create one.
                if not o_metric_map.exists():
                    o_map = MetricMappings.objects.create(metric_type_id=i_metric_type_id, source_val=s_metric_name, target_val=s_metric_name, metric_id=i_metric_id)

            else:
                o_new_metric = Metrics.objects.create(metric_type_id=i_metric_type_id, name=rec[0])
        #end for
        logger.warn('Station Type Metrics Metadata Loaded.')

    except Exception as err:
        logger.error(err)
        raise (err)


def load_station_model_metrics():
    try:
        i_metric_type_id = 3  # Station models is Metric Type 3
        with connection.cursor() as c:
            c.execute("""select distinct station_model from stationregistry_stationentry where length(station_model) > 0 
                            and station_model not in (select distinct source_val from regstats_metricmappings rm where rm.metric_type_id =3)
                        """)
            rows = c.fetchall()

        logger.warn('Loading Station Model Metadata to Metrics Table (Including mappings)')

        for rec in rows:
            o_metrics = Metrics.objects.filter(name__iexact=rec[0])

            if o_metrics.exists():
                #Get the first record as there should only be 1 distict station model from the list
                o_rec = o_metrics[0]

                #Get the metric name from the station model
                s_metric_name = o_rec.name
                i_metric_id = o_rec.metric_id

                #Check the mapping table for a record
                o_metric_map = MetricMappings.objects.filter(metric_type_id=i_metric_type_id, source_val__iexact=s_metric_name)

                #Check if we DO NOT have a mapping. if this is true, create one.
                if not o_metric_map.exists():
                    o_map = MetricMappings.objects.create(metric_type_id=i_metric_type_id, source_val=s_metric_name, target_val=s_metric_name, metric_id=i_metric_id)

            else:
                o_new_metric = Metrics.objects.create(metric_type_id=i_metric_type_id, name=rec[0])
        #end for
        logger.warn('Station Model Metrics Metadata Loaded.')

    except Exception as err:
        logger.error(err)
        raise (err)


def load_weewx_info_metrics():
    try:
        i_metric_type_id = 4  # WeeWX Info is Metric Type 4
        with connection.cursor() as c:
            c.execute(""" select distinct weewx_info from stationregistry_stationentry where length(weewx_info) > 0
                            and weewx_info not in (select distinct source_val from regstats_metricmappings rm where rm.metric_type_id = 4)
                        """)
            rows = c.fetchall()

        logger.warn('Loading WeeWX Info Metadata to Metrics Table (Including mappings)')

        for rec in rows:
            
            o_metrics = Metrics.objects.filter(name__iexact=rec[0])

            if o_metrics.exists():
                #Get the first record as there should only be 1 distict weewx_info from the list
                o_rec = o_metrics[0]

                #Get the metric name from the weewx_info
                s_metric_name = o_rec.name
                i_metric_id = o_rec.metric_id

                #Check the mapping table for a record
                o_metric_map = MetricMappings.objects.filter(metric_type_id=i_metric_type_id, source_val__iexact=s_metric_name)

                #Check if we DO NOT have a mapping. if this is true, create one.
                if not o_metric_map.exists():
                    o_map = MetricMappings.objects.create(metric_type_id=i_metric_type_id, source_val=s_metric_name, target_val=s_metric_name, metric_id=i_metric_id)

            else:
                o_new_metric = Metrics.objects.create(metric_type_id = i_metric_type_id, name=rec[0])
        #end for
        logger.warn('WeeWX Info Metrics Metadata Loaded.')

    except Exception as err:
        logger.error(err)
        raise (err)


def load_python_info_metrics():
    try:
        i_metric_type_id = 5  # Python Info is Metric Type 5
        with connection.cursor() as c:
            c.execute(""" select distinct python_info from stationregistry_stationentry where length(python_info) > 0 
                            and python_info not in (select distinct source_val from regstats_metricmappings rm where rm.metric_type_id = 5)
            """)
            rows = c.fetchall()

        logger.warn('Loading Python Info Metadata to Metrics Table (Including mappings)')

        for rec in rows:
            
            o_metrics = Metrics.objects.filter(name__iexact=rec[0])

            if o_metrics.exists():
                #Get the first record as there should only be 1 distict python_info from the list
                o_rec = o_metrics[0]

                #Get the metric name from the python_info
                s_metric_name = o_rec.name
                i_metric_id = o_rec.metric_id

                #Check the mapping table for a record
                o_metric_map = MetricMappings.objects.filter(metric_type_id=i_metric_type_id, source_val__iexact=s_metric_name)

                #Check if we DO NOT have a mapping. if this is true, create one.
                if not o_metric_map.exists():
                    o_map = MetricMappings.objects.create(metric_type_id=i_metric_type_id, source_val=s_metric_name, target_val=s_metric_name, metric_id=i_metric_id)

            else:
                o_new_metric = Metrics.objects.create(metric_type_id = i_metric_type_id, name=rec[0])
        #end for
        logger.warn('Python Info Metrics Metadata Loaded.')

    except Exception as err:
        logger.error(err)
        raise (err)


def load_platform_info_metrics():
    try:
        i_metric_type_id = 6  # Platform Info is Metric Type 6
        with connection.cursor() as c:
            c.execute(""" select distinct platform_info from stationregistry_stationentry where length(platform_info) > 0 
                            and platform_info not in (select distinct source_val from regstats_metricmappings rm where rm.metric_type_id = 6)
                        """)
            rows = c.fetchall()

        logger.warn('Loading Platform Info Metadata to Metrics Table (Including mappings)')

        for rec in rows:
            
            o_metrics = Metrics.objects.filter(name__iexact=rec[0])

            if o_metrics.exists():
                #Get the first record as there should only be 1 distict Platform Info from the list
                o_rec = o_metrics[0]

                #Get the metric name from the platform_info
                s_metric_name = o_rec.name
                i_metric_id = o_rec.metric_id

                #Check the mapping table for a record
                o_metric_map = MetricMappings.objects.filter(metric_type_id=i_metric_type_id, source_val__iexact=s_metric_name)

                #Check if we DO NOT have a mapping. if this is true, create one.
                if not o_metric_map.exists():
                    o_map = MetricMappings.objects.create(metric_type_id=i_metric_type_id, source_val=s_metric_name, target_val=s_metric_name, metric_id=i_metric_id)

            else:
                o_new_metric = Metrics.objects.create(metric_type_id=i_metric_type_id, name=rec[0])
        #end for
        logger.warn('Platform Info Metrics Metadata Loaded.')

    except Exception as err:
        logger.error(err)
        raise (err)

# ===== Attribute enrichment function =====
def update_metadata_attribs():
    try:
        with connection.cursor() as cursor:


            # --- Platform_info (Metric Type#6) - attribute#1 (O/S) ---
            cursor.execute("update regstats_metrics set attrib1 = 'Debian' where metric_type_id = 6 and upper(name) like UPPER('%%debian%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'Ubuntu' where metric_type_id = 6 and upper(name) like UPPER('%%UBUNTU%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'CentOS' where metric_type_id = 6 and upper(name) like UPPER('%%CENTOS%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'SuSE' where metric_type_id = 6 and upper(name) like UPPER('%%SUSE%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'Fedora' where metric_type_id = 6 and upper(name) like UPPER('%%FEDORA%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'MS-Windows' where metric_type_id = 6 and upper(name) like UPPER('%%WINDOWS%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'Mandrake' where metric_type_id = 6 and upper(name) like UPPER('%%MANDRAKE%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'Linux Mint' where metric_type_id = 6 and upper(name) like UPPER('%%LINUXMINT%%')")
            cursor.execute("update regstats_metrics set attrib1 = 'Other' where metric_type_id = 6 and attrib1 is NULL")

            # --- Platform_info (Metric Type#6) - attribute#2 (Architecture) ---
            cursor.execute("update regstats_metrics set attrib2 = 'ARM' where metric_type_id = 6 and UPPER(name) like UPPER('%%armv%%')")
            cursor.execute("update regstats_metrics set attrib2 = 'x86 64bit' where metric_type_id = 6 and UPPER(name) like UPPER('%%x86_64%%')")
            cursor.execute("update regstats_metrics set attrib2 = 'i686' where metric_type_id = 6 and UPPER(name) like UPPER('%%i686%%')")
            cursor.execute("update regstats_metrics set attrib2 = 'Other' where metric_type_id = 6 and attrib2 is NULL")
            
    except Exception as err:
        logger.error(err)
        raise err


# ===== Bundled functions =====
def load_geo_metadata():
    try:
        #First get all distinct location data from the stations table
        with connection.cursor() as c:
            c.execute(""" select distinct latitude, longitude, location_country_code, location_province, location_city 
                          from stationregistry_stations
                          where LENGTH(location_country_code) > 0 
                          AND LENGTH(location_province) > 0 
                          AND LENGTH(location_city) > 0
                          AND (location_country_code, location_province, location_city) not in (select distinct rg.source_country_code, rg.source_province, rg.source_city from regstats_geographymappings rg) 
                    """)
            rows = c.fetchall()
        
        logger.warn('loading geography metadata')
        #now iterate through the lsit to see if we have a Geography record
        for rec in rows:
            g = Geography.objects.filter(country_code__iexact=rec[2], province__iexact=rec[3], city__iexact=rec[4])
            
            #Check to see if this record already exists in the Geography table
            if g.exists():
                g_rec = g[0]
                i_geo_id = g_rec.geo_id
                
                gm = GeographyMappings.objects.filter(latitude=rec[0], longitude=rec[1], source_country_code__iexact=rec[2], source_province__iexact=rec[3], source_city__iexact=rec[4])
            
                if gm.exists():
                    pass
                else:
                    o = GeographyMappings.objects.create(latitude=rec[0], 
                                                        longitude=rec[1], 
                                                        source_country_code=rec[2],
                                                        source_province=rec[3], 
                                                        source_city=rec[4],
                                                        target_country_code=rec[2],
                                                        target_province=rec[3],
                                                        target_city=rec[4],
                                                        geo_id = i_geo_id)
            else:
                og = Geography.objects.create(country_code=rec[2],
                                            province=rec[3], 
                                            city=rec[4],)
                i_geo_id = og.geo_id
                o = GeographyMappings.objects.create(latitude=rec[0], 
                                    longitude=rec[1], 
                                    source_country_code=rec[2],
                                    source_province=rec[3], 
                                    source_city=rec[4],
                                    target_country_code=rec[2],
                                    target_province=rec[3],
                                    target_city=rec[4],
                                    geo_id = i_geo_id)
        #END FOR
        logger.warn('metadata loaded')

    except Exception as err:
        logger.error(err)
        raise err


def load_stats_metadata():
    load_station_type_metrics()
    load_station_model_metrics()
    load_weewx_info_metrics()
    load_python_info_metrics()
    load_platform_info_metrics()

    #enrich the metric attributes
    update_metadata_attribs()