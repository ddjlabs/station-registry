import os
import base64
import decimal
import logging
import re
import requests
import urllib3
import urllib.parse as ul
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse

import urllib3.connectionpool
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone

from .models import Stations, URLBlackList, StationEntry

logger = logging.getLogger(__name__)


def sanitize(s_val: str):
    if s_val is None:
        return ''
    else:
        return s_val


def get_my_timezone_date(original_datetime):
    tz = timezone.get_current_timezone()
    timezone_datetime = timezone.make_aware(original_datetime, tz, True)
    return timezone_datetime


def validate_lat_long(lat: str, long: str):
    try:
        b_valid_coordinates = True
        s_message = []

        # Latitude Check: Make sure it is convertible to a Decimal Value and its bounds between 90 and -90
        try:
            dec_lat = Decimal(str(lat))

            if dec_lat > 90 or dec_lat < -90:
                b_valid_coordinates = False
                s_message.append(f"Latitude values are not valid. Please provide a decimal value between 90 and -90. Value provided {lat}")

        except decimal.InvalidOperation:
            b_valid_coordinates = False
            s_message.append(f"Latitude value was not a decimal value. Please provide a numeric value in the format of xx.xxxxxx. Value provided {lat}")

        # Longitude Check: Make sure it is convertible to a Decimal value and its bound between 180 and -180
        try:
            dec_long = Decimal(str(long))

            if dec_long > 180 or dec_long < -180:
                b_valid_coordinates = False
                s_message.append(f"Longitude Values are not valid. Please provide a decimal value between 180 and -180. Value provided {long}")
        except decimal.InvalidOperation:
            b_valid_coordinates = False
            s_message.append(f"Latitude value was not a decimal value. Please provide a numeric value in the format of xx.xxxxxx. Value provided {long}")

        # Report back the results
        if b_valid_coordinates:
            return True, s_message, dec_lat, dec_long
        else:
            return False, s_message, 0, 0

    except Exception as err:
        logger.error(err)
        raise err


def check_station_url(s_url: str):
    s_private_ip_regex: str = "(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)|(^169\.254\.)"
    s_error_messages: str = ''
    b_result: bool = False

    try:
        o_validator = URLValidator()
        # Try-Except for Django URL Validator
        try:

            # Validate the URL using Django's Validator
            o_validator(s_url)

            # Parse the URL so we can check the hostname
            o_url = urlparse(s_url)

            # We are only going to accept http and https protocols for urls (no FTP)
            if o_url.netloc and o_url.scheme in ('http', 'https'):

                # First see if the URL is in our blacklist table.
                if URLBlackList.objects.filter(url_name__iexact=o_url.netloc).exists():
                    b_result = False
                    s_error_messages = 'The Station''s URL Domain is not allowed for our registry. Please use a domain that you own.'
                else:
                    o_ip_check = re.search(s_private_ip_regex, o_url.netloc)

                    if o_ip_check is None:  # No match is found then it is a public URL, else it is a private URL.
                        b_result = True
                        s_error_messages = None
                    else:
                        b_result = False
                        s_error_messages = 'The Station''s URL is set to a private IP Address. Please Provide a public URL in order to register your station with WeeWX'

            # Send back results
            return b_result, s_error_messages

        except ValidationError as ValERR:
            b_result = False
            s_error_messages = str(ValERR.message)
            return b_result, s_error_messages
    except Exception as err:
        logger.error(err)
        raise err


def geo_lookup(latitude: Decimal, longitude: Decimal):
    """
    ===== Valid API Elements that come back from the Nominatim API. Documentation: https://nominatim.org/release-docs/develop/api/Reverse/ =====
    continent
    country, country_code
    region, state, state_district, county, ISO3166-2-lvl
    municipality, city, town, village, city_district, district
    borough, suburb, subdivision
    hamlet, croft, isolated_dwelling
    neighbourhood, allotments, quarter
    city_block, residential, farm, farmyard, industrial, commercial, retail
    road
    house_number, house_name
    emergency, historic, military, natural, landuse, place, railway, man_made, aerialway, boundary, amenity, aeroway, club, craft, leisure, office, mountain_pass, shop, tourism, bridge, tunnel, waterway
    postcode
    :param latitude:
    :param longitude:
    :return:
    """
    i_map_zoom_level = int(10)  # Set the Zoom level to city
    s_email_address = settings.NOMINATIM_EMAIL_ACCOUNT 

    try:
        o_location_data = {'country_code': '', 'province': 'Unknown', 'city': 'Unknown'}

        # We are going to use Nominatim Reverse Lookup API to determine Country, Province,
        # and City based on the station's LAT/LONG.
        # Documentation: https://nominatim.org/release-docs/develop/api/Reverse/

        if latitude == 0 and longitude == 0:
            return o_location_data['country_code'], o_location_data['province'], o_location_data['city']

        try:
            s_map_url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}&zoom={i_map_zoom_level}&email={s_email_address}'

            # Make API Call for data and parse it
            req = requests.get(s_map_url).json()

            if 'error' in req:
                o_location_data['country_code'] = ''
                o_location_data['province'] = 'Unknown'
                o_location_data['city'] = 'Unknown'
            else:
                # Country Mapping
                if 'country_code' in req['address']:
                    o_location_data['country_code'] = str(req['address']['country_code'])
                else:
                    o_location_data['country_code'] = ''

                # State/Province mapping
                if 'state' in req['address']:
                    o_location_data['province'] = str(req['address']['state'])
                elif 'state_district' in req['address']:
                    o_location_data['province'] = str(req['address']['state_district'])
                elif 'region' in req['address']:
                    o_location_data['province'] = str(req['address']['region'])
                else:
                    o_location_data['province'] = 'Unknown'

                # City mapping
                # municipality, city, town, village, city_district, district
                if 'municipality' in req['address']:
                    o_location_data['city'] = str(req['address']['municipality'])
                elif 'city' in req['address']:
                    o_location_data['city'] = str(req['address']['city'])
                elif 'town' in req['address']:
                    o_location_data['city'] = str(req['address']['town'])
                elif 'village' in req['address']:
                    o_location_data['city'] = str(req['address']['village'])
                elif 'city_district' in req['address']:
                    o_location_data['city'] = str(req['address']['city_district'])
                elif 'district' in req['address']:
                    o_location_data['city'] = str(req['address']['district'])
                # elif 'county' in req['address']:   #NOTE: WE ARE NOT GOING TO MAP COUNTY TO CITY. IT WILL CONFUSE USERS!
                #    o_location_data['city']= str(req['address']['county'])
                else:
                    o_location_data['city'] = 'Unknown'

        except ConnectTimeout:
            o_location_data['country_code'] = None
            o_location_data['province'] = None
            o_location_data['city'] = None

        # Send back the results
        return o_location_data['country_code'], o_location_data['province'], o_location_data['city']

    except Exception as err:
        logger.error(err)
        raise err


def check_url(station_url: str):
    i_timeout_secs: int = 10

    try:
        # Check the URL by executing a GET request. Do this in a try/except to capture the ConnectTimeout exception
        try:
            request = requests.get(station_url, timeout=i_timeout_secs)

            if request.status_code == 200:
                return True
            else:
                return False
        except:
            # if it times out, it is not reachable thus we will consider it bad.
            return False

    except Exception as err:
        logger.error(err)
        raise err


def validate_data(value: str, str_max_length: int):
    if value is not None:
        if len(value) > str_max_length:
            return False
        else:
            return True
    else:
        return False


def process_station_entry(dict_station_request, client_ip_address : str):
    b_valid_url: bool = False
    b_valid_coordinates: bool = False
    b_valid_entry: bool = False
    b_valid_data: bool = True
    dt_entry_ts: datetime = timezone.now()
    i_station_status = 1  # All new station records will be set to unknown until URL is verified.

    try:
        s_msg = []

        #Validate the model to ensure we have all fields

        #Station URL Length Check
        if not validate_data(dict_station_request['station_url'], 250):
            s_msg.append('Station URL value is too long. Please shorten under 250 characters')
            b_valid_data = False

        #latitude Check
        if not 'latitude' in dict_station_request:
            s_msg.append('Please provide a latitude for this station')
            b_valid_data = False
        
        #Longitude Check
        if not 'longitude' in dict_station_request:
            s_msg.append('Please provide a longitude for this station')
            b_precheck_dict = False

        #Station Type Check
        if not 'station_type' in dict_station_request:
            s_msg.append('Please provide the station type for this station')
            b_valid_data = False
        else:
            if not validate_data(dict_station_request["station_type"], 100):
                s_msg.append('Station Type value is too long. Please shorten under 100 characters')
                b_valid_data = False
        
        #Station Model Check
        if not 'station_model' in dict_station_request:
            s_msg.append('Please provide the station model this station')
            b_valid_data = False
        else:
            if not validate_data(dict_station_request["station_model"], 150):
                s_msg.append('Station Model value is too long. Please shorten under 150 characters')
                b_valid_data = False
        
        #WeeWX Info Check
        if not 'weewx_info' in dict_station_request:
            s_msg.append('Please provide the WeeWX Version for this station')
            bb_valid_data = False
        else:
            if not validate_data(dict_station_request["weewx_info"], 64):
                s_msg.append('WeeWX Info value is too long. Please shorten under 64 characters')
                b_valid_data = False

        #Python Info Check
        if not 'python_info' in dict_station_request:
            s_msg.append('Please provide the python version for this station')
            b_valid_data = False
        else:
            if not validate_data(dict_station_request["python_info"], 64):
                s_msg.append('Python Info value is too long. Please shorten under 64 characters')
                b_valid_data = False

        #Platform Info Check
        if not 'platform_info' in dict_station_request:
            s_msg.append('Please provide platform information for this station')
            b_valid_data = False
        else:
            if not validate_data(dict_station_request["platform_info"], 150):
                s_msg.append('Platform Info value is too long. Please shorten under 150 characters')
                b_valid_data = False

        #Station Description Check
        if not 'description' in dict_station_request:
            s_msg.append('Please provide the station description')
            b_valid_data = False
        else:
            if not validate_data(dict_station_request["description"], 255):
                s_msg.append('Station Description value is too long. Please shorten under 255 characters')
                b_valid_data = False


        if b_valid_data:
            # Check the Station URL First to make sure it is valid before we even proceed.
            b_valid_url, s_result = check_station_url(dict_station_request["station_url"])

            if b_valid_url:
                # check the latitude and longitude values to make sure they are valid
                b_valid_coordinates, s_result, dec_lat, dec_long = validate_lat_long(dict_station_request["latitude"],
                                                                                dict_station_request["longitude"])

                if b_valid_coordinates:

                    # Now Validate the rest of the records
                    s_station_url = str(dict_station_request["station_url"])
                    s_description = str(dict_station_request["description"])
                    s_station_type = str(dict_station_request["station_type"])
                    s_station_model = str(dict_station_request["station_model"])
                    s_weewx_info = str(dict_station_request["weewx_info"])
                    s_python_info = str(dict_station_request["python_info"])
                    s_platform_info = str(dict_station_request["platform_info"])
                    s_last_ip_address = str(client_ip_address)

                    # Check if the last_seen value was populated from the GET/POST request
                    if "last_seen" in dict_station_request:
                        # 2022-11-12_16:15:27
                        dt_entry_ts = get_my_timezone_date(
                            datetime.strptime(
                                str(dict_station_request["last_seen"]),
                                "%Y-%m-%d_%H:%M:%S")
                        )

                    # See if we have a Stations Record for this URL.
                    o_rec = Stations.objects.filter(station_url__iexact=s_station_url)

                    if o_rec.exists():
                        # This is to get the first record back. I only expect the first record since urls are unique
                        o_station = o_rec[0]

                        # create a Stations Entry record
                        o_entry = StationEntry.objects.create(station_id=o_station.station_id,
                                                            station_url=s_station_url,
                                                            latitude=dec_lat,
                                                            longitude=dec_long,
                                                            station_type=s_station_type,
                                                            station_model=s_station_model,
                                                            weewx_info=s_weewx_info,
                                                            python_info=s_python_info,
                                                            platform_info=s_platform_info,
                                                            description=s_description,
                                                            last_ip_address=s_last_ip_address,
                                                            entry_dt=dt_entry_ts)

                        # Check and see if the latitude and/or longitude changed.
                        # if so, run the geolocate function to populate the location fields
                        if o_station.latitude != dec_lat or o_station.longitude != dec_long:
                            loc_country_code, loc_province, loc_city = geo_lookup(dec_lat, dec_long)

                            o_station.location_country_code = loc_country_code
                            o_station.location_province = loc_province
                            o_station.location_city = loc_city
                        # END coordinate check

                        # Update Stations Table with the same information and set the last check in datetime to the entry datetime
                        o_station.latitude = dec_lat
                        o_station.longitude = dec_long
                        o_station.station_type = s_station_type
                        o_station.station_model = s_station_model
                        o_station.weewx_info = s_weewx_info
                        o_station.python_info = s_python_info
                        o_station.platform_info = s_platform_info
                        o_station.description = s_description
                        o_station.last_ip_address = s_last_ip_address
                        o_station.last_entry_dt = dt_entry_ts
                        o_station.save()

                        s_msg.append('Station Registry Updated')
                        b_valid_entry = True
                    else:
                        # Perform Geo Lookup to obtain the Country Code, Province/State, and City based on the lat/long provided
                        loc_country_code, loc_province, loc_city = geo_lookup(dec_lat, dec_long)

                        # Create the Stations Record First
                        o_station = Stations.objects.create(station_url=s_station_url,
                                                            latitude=dec_lat,
                                                            longitude=dec_long,
                                                            location_country_code=loc_country_code,
                                                            location_province=loc_province,
                                                            location_city=loc_city,
                                                            station_type=s_station_type,
                                                            station_model=s_station_model,
                                                            weewx_info=s_weewx_info,
                                                            python_info=s_python_info,
                                                            platform_info=s_platform_info,
                                                            description=s_description,
                                                            last_ip_address=s_last_ip_address,
                                                            register_dt=dt_entry_ts,
                                                            last_entry_dt=dt_entry_ts,
                                                            station_status_id=i_station_status)

                        # Ensure we have a Station ID provided when the record was created. It is needed for the entry table.
                        if o_station.station_id is not None:

                            # create a Stations Entry record
                            o_entry = StationEntry.objects.create(station_id=o_station.station_id,
                                                                station_url=s_station_url,
                                                                latitude=dec_lat,
                                                                longitude=dec_long,
                                                                station_type=s_station_type,
                                                                station_model=s_station_model,
                                                                weewx_info=s_weewx_info,
                                                                python_info=s_python_info,
                                                                platform_info=s_platform_info,
                                                                description=s_description,
                                                                last_ip_address=s_last_ip_address,
                                                                entry_dt=dt_entry_ts)
                        else:
                            s_msg.append('There was an issue saving the Station Entry Record. Please report to WeeWX Developers group.')
                            b_valid_entry = False

                        # Report back that the station is created
                        s_msg.append('Station registered in the WeeWX Station Registry')
                        b_valid_entry = True
                else:
                    for i in s_result:
                        s_msg.append(i)
                    
                    b_valid_entry = False
                # END Coordinate Checks
            else:
                s_msg.append(s_result)
                b_valid_entry = False
        else:
            b_valid_entry = False
        # End b_valid_entry Check


        # Return the result of the entry attempt (Boolean) and any validation messages back to the API View
        return b_valid_entry, s_msg

    except Exception as err:
        logger.error(err)
        raise err


def render_site_profile_image(o_station: object):
    try:
        dt_entry_ts: datetime = timezone.now()
        
        logger.info('starting image generation')

        # It's possible to make requests without the api key, but the number of requests is very limited  
        s_station_url = str(o_station.station_url)

        s_url_expanded = ul.quote_plus(s_station_url)
        
        #Create the image name by generating a hash based on the station url. The image path will go in the MEDIA_ROOT folder.
        s_image_name = str(abs(hash(s_station_url))) + '.jpg'
        s_image_path = os.path.join(settings.STATION_IMAGES_LOCATION, s_image_name)

        logger.info(f"Station image Path is {s_image_path}")

        #Prep the API call to Google's Page Speed Tool 
        google_api_key = settings.GOOGLE_API_KEY
        s_api_call = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={s_url_expanded}&key={google_api_key}"
        logger.info(f'API Call is = {s_api_call}')
        
        #Make the API call to Google and parse out the JSOn response.
        try:
            response = requests.get(s_api_call)

            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
                json_result = response.json()
                logger.info('received json response from Google Page Analytics. Decoding image byte data')
                
                ss_encoded = json_result['lighthouseResult']['audits']['final-screenshot']['details']['data'].replace("data:image/jpeg;base64,", "")
                ss_decoded = base64.b64decode(ss_encoded)

                logger.info('Image decoded')
                
                #Write out the decoded bytes as a jpeg site profile image.
                f = open(s_image_path, 'wb+')
                f.write(ss_decoded)
                f.close()

                logger.info(f'image saved to filesystem at {s_image_path}')
                
                #Update the Station record with the image name
                o_station.station_site_image = s_image_name
                o_station.site_profile_image_gen_dt = dt_entry_ts
                o_station.save()
                
                #Report back success on the image generation
                return True
            else:
                logger.info('BAD URL or not retrievable site')
                o_station.valid_url_yn=False
                o_station.last_url_check_dt=dt_entry_ts
                o_station.save()
                return True

        except Exception as err:
            raise err

    except Exception as err:
        logger.error(err)
        return False
