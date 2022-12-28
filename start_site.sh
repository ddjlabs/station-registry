#!/bin/bash

#Guide : https://medium.com/analytics-vidhya/dajngo-with-nginx-gunicorn-aaf8431dc9e0

# Name of the application
NAME="weewx"

# Django project directory
DJANGODIR=/home/doug/weewx-stationregistry/weewx

# we will communicte using this unix socket
SOCKFILE=/home/doug/run/gunicorn.sock

# the user to run as
USER=doug

# the group to run as
GROUP=doug

# how many worker processes should Gunicorn spawn
NUM_WORKERS=4

# which settings file should Django use
DJANGO_SETTINGS_MODULE=weewx.settings

# WSGI module name
DJANGO_WSGI_MODULE=weewx.wsgi 

echo "Starting $NAME as `whoami`"
# Activate the virtual environment
cd $DJANGODIR
source ../.venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn

# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../.venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-