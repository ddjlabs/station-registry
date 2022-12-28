import datetime
from datetime import datetime, timedelta
from stationregistry.models import Stations
from stationregistry import registry
from django.utils import timezone
from django.db.models import Q

import logging

logger = logging.getLogger(__name__)


def run():
    dt_entry_ts: datetime = timezone.now()
    dt_prior_entry_ts : datetime = dt_entry_ts - timedelta(days=7000)

    try:
        stations_id_list = [1, 3]  # This is for Active and unknown stations only
        logger.INFO(f'Pulling records from {dt_prior_entry_ts} to today.')
        o_unchecked_stations = Stations.objects.filter(Q(valid_url_yn=False), Q(last_url_check_dt__gte=dt_prior_entry_ts)|Q(last_url_check_dt__isnull=True))

        i_total_records = len(o_unchecked_stations)
        logger.INFO(f'{i_total_records} found to process')
        for row in o_unchecked_stations:
            # Validate the station URL is live

            logger.INFO(f'Checking Station URL {row.station_url} for a valid url')
            b_result = registry.check_url(row.station_url)

            if b_result:
                logger.INFO(f'   Station url {row.station_url} is good')
                row.last_url_check_dt = dt_entry_ts
                row.valid_url_yn = True
                row.station_status_id = 1
                row.save()
            else:
                logger.INFO(f'   Station url {row.station_url} is no bueno')
                row.valid_url_yn = False
                row.last_url_check_dt = dt_entry_ts
                row.save()
    except Exception as err:
        logger.error(err)
        raise err
