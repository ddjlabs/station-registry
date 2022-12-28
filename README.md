# WeeWX Station Registry Solution
Station Registry Solution for WeeWX. The solution collects station statistics and builds a series of dashboards to show the users where station are located as well as interesting statistics of the types of weather stations, their location data, WeeWX info, and Platform information.

## Requirements
Requirements are maintained in the requirements page here -> [requirements](docs/requirements.md)

## Design
* [Software Component Design](docs/software-design.md)
* [Data Model Design](docs/data-model-design.md)


## Installation instructions:
1. create .env file in the weewx/weewx project folder. use the sample .env.example file for guidance
2. setup a virtual environment and apply the requirements.txt file to it.
3. under the weewx/ folder start django web server by running the following command:

    ```
    python manage.py runserver
    ```


## Noteable resources

https://www.geeksforgeeks.org/how-to-install-django-with-nginx-gunicorn-and-postgresql-on-ubuntu/