import logging
from datetime import  date
from regstats import aggregator, metadata

logger = logging.getLogger(__name__)


def run():
    d_begindate : date = date(2017,10,21)
    d_enddate : date = date(2017,10,21)

    metadata.load_stats_metadata()
    metadata.load_geo_metadata()
    #aggregator.aggregate_stats(d_begindate, d_enddate)
    #aggregator.aggregate_geography(d_begindate, d_enddate)
