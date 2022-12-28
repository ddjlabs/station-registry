from rest_framework import serializers
from . models import Stations


class StationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stations
        fields = '__all__'
