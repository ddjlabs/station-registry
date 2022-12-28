import datetime
import logging
import json
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone

from stationregistry import registry
from stationregistry.models import Stations

logger = logging.getLogger(__name__)


def run():
    try:
        dt_entry_ts: datetime = timezone.now()
        dt_prior_entry_ts : datetime = dt_entry_ts - timedelta(days=30)

        logger.info('Get the data!')
        
        #This filter looks at valid urls that have a site profile image datetime that is blank or older than 30 days from today.
        o_stations = Stations.objects.filter(Q(valid_url_yn=True), Q(site_profile_image_gen_dt__lte=dt_prior_entry_ts)|Q(site_profile_image_gen_dt__isnull=True))
        
        logger.info('Received data')
        
        if o_stations.exists():
            logger.info(f"Station Exists")

            #Iterate through stations
            for o in o_stations:
                logger.info(f'analyzing station url : {o.station_url}')
                b_result = registry.render_site_profile_image(o)

                if b_result:
                    logger.info('Station image captured')
                else:
                    logger.error("Station image generation failed")
            #End For iteration of found Stations that need their site images generated.
        else:
            logger.info("No Stations Found")

    except Exception as err:
        logger.error(err)
        raise err