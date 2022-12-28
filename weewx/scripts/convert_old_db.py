import datetime
from datetime import date
import logging
from django.db import connections

from stationregistry import registry
from regstats import aggregator, metadata


logger = logging.getLogger(__name__)


def run():
    try:

        d_begindate : date = date(2017,10,21)
        d_enddate : date = date(2017,10,31)


        s_old_data : str = """
                            select DISTINCT 
                                station_url ,
                                description ,
                                latitude ,
                                longitude ,
                                station_type ,
                                station_model ,
                                weewx_info ,
                                python_info ,
                                platform_info ,
                                last_addr ,
                                FROM_UNIXTIME(last_seen, '%Y-%m-%d_%h:%i:%s') as last_seen_dt
                            from weereg.stations
                            where date(FROM_UNIXTIME(last_seen, '%Y-%m-%d')) between date('{0}') and date('{1}')
                            order by FROM_UNIXTIME(last_seen, '%Y-%m-%d_%h:%i:%s'), station_url, latitude, longitude asc
                            """.format(d_begindate.strftime('%Y-%m-%d'),d_enddate.strftime('%Y-%m-%d'))

        with connections['old_db'].cursor() as cursor:
            cursor.execute(s_old_data)
            row = cursor.fetchall()

            d_procdate : date = d_begindate

            for r in row:
                s_temp = registry.sanitize(r[10]).split('_')
                d_curdate : date = datetime.datetime.strptime(s_temp[0],'%Y-%m-%d').date()


                dict_station_request = {"station_url": registry.sanitize(r[0]), "description": registry.sanitize(r[1]),
                                        "latitude": registry.sanitize(r[2]), "longitude": registry.sanitize(r[3]),
                                        "station_type": registry.sanitize(r[4]), "station_model": registry.sanitize(r[5]),
                                        "weewx_info": registry.sanitize(r[6]), "python_info": registry.sanitize(r[7]),
                                        "platform_info": registry.sanitize(r[8]),
                                        "last_ip_address": registry.sanitize(r[9]), "last_seen": registry.sanitize(r[10])}

                logger.warning(f'Station URL: {r[0]} | Station Lat: {r[2]} | Station Long: {r[3]} | Last Seen : {r[10]}')

                logger.warning('Posting record to new registry')
                b_result, s_message = registry.process_station_entry(dict_station_request)

                logger.warning(f'result was {b_result} with message : {s_message}')

                #Check to see if the current date is now different than process date. 
                if d_curdate != d_procdate:
                    metadata.load_stats_metadata()
                    aggregator.aggregate_stats(d_curdate, d_curdate)
                    metadata.load_geo_metadata()
                    aggregator.aggregate_geography(d_curdate, d_curdate)
                    
                    d_procdate = d_curdate
            # end Row Loop
            #
            
        #End WITH

        #Now Build Stats for the entire process

    except Exception as err:
        logger.error(err)
        raise (err)
