from rest_framework import serializers
from . models import Stations, StationEntry


class StationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stations
        fields = '__all__'

class StationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StationEntry
        fields = '__all__'
