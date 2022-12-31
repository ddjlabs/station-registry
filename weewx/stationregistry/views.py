import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from rest_framework import viewsets, request, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from . import registry
from . models import Stations, StationEntry, StationExtensions
from .serializers import StationsSerializer, StationEntrySerializer


class StationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stations to be viewed and edited
    """
    queryset = Stations.objects.all()
    serializer_class = StationsSerializer


class StationEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stations to be viewed and edited
    """
    queryset = StationEntry.objects.all()
    serializer_class = StationEntrySerializer


@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def register_cgi(request):
    """
    Register Station (old CGI Method)
    This is to replicate the existing PERL Process. Please see (http://weewx.com/register/register.cgi?weewx_info=2.6.0a5&python_info=3.10.2)
    Note: We are going to throttle this API Endpoint to no more than 10 requests/day. 
    """
    try:
        dict_station_request = {}
        dict_station_request = request.GET

        #We must have a station url in the GET Parameters in order to proceed. if not, reject it compeletly.
        if 'station_url' in dict_station_request:

            #Get the client's IP address from the request object
            request_ip, is_routable = get_client_ip(request)
            
            #Process the request
            b_result, s_msg = registry.process_station_entry(dict_station_request, request_ip)

            #parse all the validation messages to JSON so that the client can parse it in its logs
            json_result = json.dumps(s_msg)

            #Check the result of the request.
            if b_result:
                return Response({"OK", json_result}, status=status.HTTP_200_OK)
            else:
                return Response({"FLOP", json_result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"FLOP", "No Station URL"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as err:
        raise err
    
