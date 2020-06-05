from rest_framework import serializers

from .models import GasStation
from .models import Fuel
from .models import Service
from .models import FuelStation
from .models import ServiceStation


class GasStationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = ('lat', 'lon', 'number', 'region', 'city', 'street',
                  'building', 'zip_code')


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = ('name', 'image')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'image')


class ServiceStationSerializer(serializers.ModelSerializer):
    services = ServiceSerializer()

    class Meta:
        model = ServiceStation
        fields = ('services', 'price')


class FuelStationSerializer(serializers.ModelSerializer):
    fuels = FuelSerializer()

    class Meta:
        model = FuelStation
        fields = ('fuels', 'price', 'currency')


class GasStationSerializer(serializers.ModelSerializer):
    fuel = FuelSerializer(read_only=True, many=True)
    service = ServiceSerializer(read_only=True, many=True)

    class Meta:
        model = GasStation
        fields = '__all__'
