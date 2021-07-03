#!/bin/bash
# -*- coding: utf-8 -

NAME="hx2Site"                              #Name of the application (*)
DJANGODIR=/var/www/hx2/hx2Site/            # Django project directory (*)
SOCKFILE=/var/www/hx2/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=www-data                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=hx2Site.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=hx2Site.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
