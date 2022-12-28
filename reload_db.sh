cd weewx
python manage.py reset_db --no-input
python manage.py migrate

python manage.py loaddata station_status
python manage.py loaddata url_blacklist
python manage.py loaddata metric_types
python manage.py loaddata metrics

"""
These statements need to run on the database before we start django. 
TODO: For some reason the migrations do not create the default timestamps on MariaDB. Need to investigate further

ALTER TABLE weereg_lab2.regstats_metrics MODIFY COLUMN lst_updt_ts datetime(6) DEFAULT now() NOT NULL;
ALTER TABLE weereg_lab2.regstats_metricmappings MODIFY COLUMN lst_updt_ts datetime(6) DEFAULT now() NOT NULL;
ALTER TABLE weereg_lab2.regstats_metrictypes MODIFY COLUMN lst_updt_ts datetime(6) DEFAULT now() NOT NULL;
ALTER TABLE weereg_lab2.regstats_geography MODIFY COLUMN lst_updt_ts datetime(6) DEFAULT now() NOT NULL;
ALTER TABLE weereg_lab2.regstats_geographymappings MODIFY COLUMN lst_updt_ts datetime(6) DEFAULT now() NOT NULL;
"""
