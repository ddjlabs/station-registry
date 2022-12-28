# WeeWX Station Registry v2 Requirements
Last Update: 12-27-2022

## Goals
1. Replace the existing PERL solution located at weewx.com/register with a REST API. Solution should be written in a language that can be supported by fellow maintainers of WeeWX.
2. The replacement solution must accept and process existing weather station check in. The existing check in process is the following:

    2.1 Each station checks in upon start up or every 1 day (86400 seconds)    
    2.2 Stations check in to http://www.weewx.com/register/register.cgi via a GET or POST method    
    2.3 The station will provide the following data elements as a querystring to the existing check-in process:
    
        station url
        Station Type
        Station Model
        Description
        WeeWX info
        Python Info
        Platform Info
        Latitude
        Longitude

    2.4 The existing solution sends a http response of 200 with the value of "Ok, "Updated" when successful. if there is a failure, the existing solution sends a 405 with the value of "FLOP, Error".

3. The new solution should provide REST endpoint for future WeeWX weather stations to use. This endpoint should be either a PUT or UPDATE method where the new registry sends back a correct response (200 succesful, 405 error, 429 too many attempts). The REST solution should send a JSON request and receive a JSON response.

4. The new solution should limit weather stations to report no more than once per day. If in the event they report more than once a day, a http response of 429 should be sent back.

5. The new solution should accept the config_path and entry_path values from the WeeWX Weather station and store it in the database per submission.

6. All stations should have a unique, public addressable url. The new solution should validate the url with the following methods:

    6.1 Verify that the url is not a private url. a Private url is when it contains a private network such as 192.168.x.x, 172.16.x.x, 10.x.x.x, 169.258.x.x

    6.2 Verify that the url is not on a blacklist. The URL blacklist should be maintained in a table within the station registry database. The URL blacklist should be managable by the WeeWX maintainers via a web interface.

7. All stations should have a valid latitude and longitude. The solution will validate the results and send back an error to the weather station if the values are invalid.

8. **NewRequirement** Extension reporting:  for the REST API, WeeWX restx will be modified to include the current list of extensions installed per submission. this will include the extension name, extension version, and extension description. This information will be retained in a separate table and will be reported on each check-in. This will be only for the WeeWX release that includes this update.

## Infrastructure requirements

9. The new solution should not require additional infrastructure. It should run using a AWS Lightsail instance with 1GB of RAM and 1 vCPU. The solution should not interfere with the existing software configuration and deployment of WeeWX.com or other tools/utilities on the server.

10. The new solution should share the NGINX Web Server with WeeWX.com 

11. The new solution should use MySQL as it primary database backend. Appropriate backups should be configured to ensure recovery in the event of a systemic failure.


## **NewRequirement** Location mapping

12. The solution should upon a new station's registration, look up the country, state or province, and city based on the provided latitude and longitude.

13. The new solution will interface with OpenStreetMap WebAPI to determine location information

14. The location data will only be retrieved when a station is first registered or if the stations' latitude or longitude values change during a station check in operation.

15. Location Data will be aggregated and reported in WeeWX station registry stats pages. 

16. Location Data will be used as filters for the WeeWX Station Map at WeeWX.com. This will allow users to find local stations based on Country, State/Province, and City. 

## Reporting Requirements
17. The solution should collect, map, and report statistical counts based on the following fields:


    Station Status (Active | Stale)
    
    Station Type
    
    Station Model
    
    WeeWX Info
    
    Python Info
    
    Platform Info
    
    Location Country
    
    Location State/Province
    
    Location City


18. On a daily basis (12:01AM), these statistics should be aggregated and reported into the Station Registry Database. This will be a batch process scheduled by cron. The batch process will update the mapping and metadata tables within the database and load the prior day's results into the FACT tables.

19. These values should be presented as a series of graphs and dashboards on the WeeWX.com website. The graphs and results should be interactive and dynamic to the web user. The following graphs and data reports should be available to the user:

### Current State
* Total Stations by Station Status (Active | Stale | disabled). This output should have a user-defined filter by country, province/state, and city.

* Total Stations by WeeWx Info. The graph should provide results in precentages based on WeeWX major releases (eg 2.x, 3.x, 4.x, etc)

* Total Stations by Weather Station Hardware. This should be a Pie chart showing percentages by major weather station manufacturers (eg. Davis, Acurite, Ecowitt, SDR, etc.).

* Total Station by Platform. The pie graph will show stations by distribution type (eg Debian, Raspberry Pi, FreeBSD, Ubuntu, Arch, etc.).

* Total Stations by Python version. This should be a pie chart showing percentages by major Python releases (2.x, 3.x).

* Station Reporting Activity: Metric that will display the total number of stations reporting over the past 24 hours with a percentage of total active stations reporting in. (total reported/Total active stations).

### Historical Stats
* Stations by Status : Chart that will show over the past 24 months how many active and stale stations are using WeeWX. Filter by status

* Stations by WeeWX Version: Chart that will show over the past 24 months how many stations by WeeWX version. Filter by Weewx Version, WeeWx Major Version.

* Stations by Python Version: Chart that will show over the past 24 months how many stations are on which versions of Python. Filter by Major release

* Stations by Platform: Chart taht will show over the past 24 months how manyu stations are using which plathform. Filter by O/S, Architecture, and Platform Info.

## Station Registry Checks and Maintenance

20. On a daily basis, the Station Registry will update active stations status from active to stale if the station has not reported a check-in in over 30 days. This will be a scheduled event via cron that will happen at 1:00AM Server Time.

21. On a daily basis, the station registry will check to see URLS that have not been scanned in the last 28 days. The check will be to attempt to go to the url. if a http response of 200 occurs, the url will remain active. if there is no response from the url, the station registry will be updated to show the station url is not available. unavailable urls will not have active links in the station map or reporting. This will be a scheduled event in cron that will happen at 1:30AM Server Time.

22. On a daily basis, the station registry will check for active stations that do not have a site profile image. If it finds a station that is active (URL is verified) and does not have a image, it will use Google Page Analytics to scan the site and retrieve the image from the request. The image will be stored in the station profile images and the image will be linked to the registry. This will be a scheduled event in cron that will happen at 2:30am server time.

## **New Requirement** Registry Management

23. The Station Registry will require a user interface to manage the URL Blacklist and mappings for station values to the aggregated reported values. This interface will perform CRUD operations on the items mentioned above. 

24. The interface needs to be secure with the ability to grant each user a username & password from the command line.
