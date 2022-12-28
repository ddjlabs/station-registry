import logging
import datetime
from django.conf import settings
from django.db import connection
from datetime import date
from .models import GeographyMappings, Geography, Metrics, MetricMappings
from stationregistry.models import StationEntry

logger = logging.getLogger(__name__)


def clear_metric_stats(d_begindate: date, d_enddate: date, metric_type_id : int):
    try:
        s_sql : str = """
                        delete from regstats_stationstats 
                            where stat_id in (select rs.stat_id 
                                            from regstats_stationstats rs 
                                            inner join regstats_metrics rm on rs.metric_id = rm.metric_id 
                                            where rm.metric_type_id = {2} 
                                            and rs.report_dt between date('{0}') and date('{1}'))
                        """.format(d_begindate.strftime('%Y-%m-%d'),d_enddate.strftime('%Y-%m-%d'), metric_type_id)
        with connection.cursor() as cursor:
            cursor.execute(s_sql)

    except Exception as err:
        logger.error(err)
        raise err


def aggregate_stats(d_begindate : date, d_enddate: date):
    try:

        i_stale_limit : int = settings.STATION_STALE_LIMIT_DAYS
        i_purge_limit : int = settings.STATION_PURGE_LIMIT_DAYS

        d_delta = datetime.timedelta(days=1)

        with connection.cursor() as cursor:
            while(d_begindate <= d_enddate):
                print(d_begindate)

                # === Stations Counts (active / stale)
                s_sql_1 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, data_val) 
                                (select 
                                    date('{0}') as rpt_date,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS METRIC_ID,	
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    where date(entry_dt) <= date('{0}')
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY)   
                                    group by stations_id) a
                                group by station_status)
                                """.format(d_begindate.strftime('%Y-%m-%d'),i_stale_limit, i_purge_limit)
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 1)
                
                #Execute Station status load
                cursor.execute(s_sql_1)



                # === Station Type Load
                s_sql_2 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, DATA_VAL) 
                                (select 
                                    date('{0}') as rpt_date,
                                    a.metric_id,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, station_type, mm.metric_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    inner join regstats_metricmappings mm on mm.source_val = ss.station_type and mm.metric_type_id = 2
                                    where date(entry_dt) <= date('{0}')
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY)   
                                    group by stations_id) a
                                group by a.metric_id
                                order by a.station_type asc)
                                """.format(d_begindate.strftime('%Y-%m-%d'),i_stale_limit, i_purge_limit)
                
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 2)
                
                #Execute Station status load
                cursor.execute(s_sql_2)
                


                # === Station Model Load
                s_sql_3 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, DATA_VAL) 
                                (select 
                                    date('{0}') as rpt_date,
                                    a.metric_id,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, station_model, mm.metric_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    inner join regstats_metricmappings mm on mm.source_val = ss.station_model and mm.metric_type_id = 3
                                    where date(entry_dt) <= date('{0}')	  
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY)  
                                    group by stations_id) a
                                group by a.metric_id
                                order by a.station_model asc)
                                """.format(d_begindate.strftime('%Y-%m-%d'),i_stale_limit, i_purge_limit)
                
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 3)
                
                #Execute Station status load
                cursor.execute(s_sql_3)



                 # === WeeWX Info Load
                s_sql_4 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, DATA_VAL) 
                                (select 
                                    date('{0}') as rpt_date,
                                    a.metric_id,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, weewx_info, mm.metric_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    inner join regstats_metricmappings mm on mm.source_val = ss.weewx_info and mm.metric_type_id = 4
                                    where date(entry_dt) <= date('{0}')	  
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY) 
                                    group by stations_id) a
                                group by a.metric_id
                                order by a.weewx_info asc);
                                """.format(d_begindate.strftime('%Y-%m-%d'),i_stale_limit, i_purge_limit)
                
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 4)
                
                #Execute Station status load
                cursor.execute(s_sql_4)



                 # === Python Info Load
                s_sql_5 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, DATA_VAL) 
                                (select 
                                    date('{0}') as rpt_date,
                                    a.metric_id,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, python_info, mm.metric_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    inner join regstats_metricmappings mm on mm.source_val = ss.python_info and mm.metric_type_id = 5
                                    where date(entry_dt) <= date(@procdate)
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY) 
                                    group by stations_id) a
                                group by a.metric_id
                                order by a.python_info asc);
                                """.format(d_begindate.strftime('%Y-%m-%d'),i_stale_limit, i_purge_limit)
                
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 5)
                
                #Execute Station status load
                cursor.execute(s_sql_5)


                 # === Platform Info Load
                s_sql_6 : str = """
                                insert into regstats_stationstats (report_dt, metric_id, station_status_id, DATA_VAL) 
                                (select 
                                    date('{0}') as rpt_date,
                                    a.metric_id,
                                    CASE 
                                        WHEN date(a.last_record) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                        ELSE 2 -- stale
                                    END AS STATION_STATUS,	
                                    count(*) as metric_count
                                from( select distinct stations_id, platform_info, mm.metric_id, MAX(entry_dt) as LAST_RECORD
                                    from stationregistry_stationentry ss
                                    inner join regstats_metricmappings mm on mm.source_val = ss.platform_info and mm.metric_type_id = 6
                                    where date(entry_dt) <= date('{0}')
                                    and date(entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY) 
                                    group by stations_id) a
                                group by a.metric_id
                                order by a.platform_info asc)
                                """.format(d_begindate.strftime('%Y-%m-%d'), i_stale_limit, i_purge_limit)
                
                #Clear intersections before loading
                clear_metric_stats(d_begindate,d_enddate, 6)
                
                #Execute Station status load
                cursor.execute(s_sql_6)


                #increment the begin date value
                d_begindate += d_delta
            #END WHILE

    except Exception as err:
        logger.error(err)
        raise err


def aggregate_geography(d_begindate : date, d_enddate: date):
    try:
        i_stale_limit : int = settings.STATION_STALE_LIMIT_DAYS
        i_purge_limit : int = settings.STATION_PURGE_LIMIT_DAYS

        d_delta = datetime.timedelta(days=1)

        with connection.cursor() as cursor:
            while(d_begindate <= d_enddate):
                print(d_begindate)
                s_sql = """
                            insert into regstats_geostats (report_dt, station_status_id, geo_id, data_val)
                            (select 
                                date('{0}') as rpt_date,
                                CASE 
                                    WHEN date(ss.last_entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {1} DAY) THEN 1 -- active
                                    ELSE 2 -- stale
                                END AS STATION_STATUS,	
                                rg.geo_id, 
                                count(*) as data_val 
                            from stationregistry_stations ss
                            inner join regstats_geographymappings rg on rg.source_country_code = ss.location_country_code 
                                        and rg.source_province = ss.location_province 
                                        and rg.source_city = ss.location_city
                                        and rg.latitude = ss.latitude
                                        and rg.longitude = ss.longitude
                            where date(last_entry_dt) <= date('{0}')
                            and date(last_entry_dt) >= DATE_SUB(date('{0}'), INTERVAL {2} DAY)
                            group by rg.geo_id)
                        """.format(d_begindate.strftime('%Y-%m-%d'), i_stale_limit, i_purge_limit)
                #Clear intersections before loading
                #clear_metric_stats(d_begindate,d_enddate, 1)
                
                #Execute Station status load
                cursor.execute(s_sql)

                #increment the begin date value
                d_begindate += d_delta
        
            #END WHILE

    except Exception as err:
        logger.error(err)
        raise err

