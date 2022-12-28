#!/bin/bash

#Start Python Virtual Environment
source /.venv/bin/activate
cd weewx

#Run the script through django's engine
python3 manage.py runscript $1

#shutdown python virtual environment
if [ $? -eq 0 ]
then
    echo "Script Processed Successfully"
    exit 0
else
    echo "The Script Failed" >&2
    exit 1
fi