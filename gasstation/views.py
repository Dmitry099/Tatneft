from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GasStation
from .models import FuelStation
from .models import ServiceStation
from .models import Fuel
from .models import Service
from .serializers import GasStationsSerializer
from .serializers import GasStationSerializer
from .serializers import FuelSerializer
from .serializers import FuelStationSerializer
from .serializers import ServiceStationSerializer
from .serializers import ServiceSerializer


class GasStationsView(viewsets.ReadOnlyModelViewSet):
    """
    Список АЗС
    """
    queryset = GasStation.objects.all()
    serializer_class = GasStationsSerializer


class FuelsView(viewsets.ReadOnlyModelViewSet):
    """
    Список видов топлива
    """

    queryset = Fuel.objects.all()
    serializer_class = FuelSerializer


class ServicesView(viewsets.ReadOnlyModelViewSet):
    """
    Список видов услуг
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class GasStationView(APIView):
    """
    Полная информация по одной АЗС с учетом привязки топлива и услуг
    """

    @staticmethod
    def get(request, station_id=False, *args, **kwargs):
        if not station_id:
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Необходимо передать id АЗС в параметрах запроса'}
            )
        try:
            gas_station = GasStation.objects.prefetch_related(
                'fuel', 'service'
            ).get(id=station_id)
        except GasStation.DoesNotExist:
            return JsonResponse({
                'Status': False,
                'Error': 'АЗС с указанным id не существует'
            })
        gas_station_serializer = GasStationSerializer(gas_station)

        return Response(gas_station_serializer.data)


class FuelStationView(APIView):
    """
    Цена топлива
    """

    @staticmethod
    def get(request, station_id=False, *args, **kwargs):
        """
        Получить информацию по цене топлива для указанной АЗС
        """
        if not station_id:
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Необходимо передать id АЗС в параметрах запроса'}
            )
        try:
            fuel_stations = FuelStation.objects.select_related(
                'fuels'
            ).filter(stations_id=station_id)
        except GasStation.DoesNotExist:
            return JsonResponse({
                'Status': False,
                'Error': 'АЗС с указанным id не существует'
            })
        fuel_stations_serializer = FuelStationSerializer(fuel_stations,
                                                         many=True)

        return Response(fuel_stations_serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Добавить цену топливу
        """
        if not {'station_id', 'fuel_id',
                'price', 'currency'}.issubset(request.data):
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Не указаны все необходимые аргументы'}
            )
        station_id = request.data.get('station_id')
        fuel_id = request.data.get('fuel_id')
        price = request.data.get('price')
        currency = request.data.get('currency')
        fuel_station, created = FuelStation.objects.get_or_create(
            stations_id=station_id, fuels_id=fuel_id
        )
        fuel_station.price = price
        fuel_station.currency = currency
        fuel_station.save()
        return JsonResponse({'Status': True})


class ServiceStationView(APIView):
    """
    Цена Услуг
    """

    @staticmethod
    def get(request, station_id=False, *args, **kwargs):
        """
        Получить информацию по цене услуг для указанной АЗС
        """
        if not station_id:
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Необходимо передать id АЗС в параметрах запроса'}
            )
        try:
            service_stations = ServiceStation.objects.select_related(
                'services'
            ).filter(stations_id=station_id)
        except GasStation.DoesNotExist:
            return JsonResponse({
                'Status': False,
                'Error': 'АЗС с указанным id не существует'
            })
        service_stations_serializer = ServiceStationSerializer(service_stations,
                                                               many=True)

        return Response(service_stations_serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Добавить цену услуге
        """
        if not {'station_id', 'service_id',
                'price'}.issubset(request.data):
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Не указаны все необходимые аргументы'}
            )
        station_id = request.data.get('station_id')
        fuel_id = request.data.get('fuel_id')
        price = request.data.get('price')
        service_station, created = ServiceStation.objects.get_or_create(
            stations_id=station_id, services_id=fuel_id
        )
        service_station.price = price
        service_station.save()
        return JsonResponse({'Status': True})


class FuelView(APIView):
    """
    Топливо
    """

    @staticmethod
    def get(request, fuel_id=False, *args, **kwargs):
        """
        Получить информацию по виду топлива
        """
        if not fuel_id:
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Необходимо передать id вида топлива'
                           ' в параметрах запроса'}
            )
        try:
            fuel = Fuel.objects.get(id=fuel_id)
        except GasStation.DoesNotExist:
            return JsonResponse({
                'Status': False,
                'Error': 'Топлива с указанным id не существует'
            })
        fuel_serializer = FuelSerializer(fuel)

        return Response(fuel_serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Добавить вид топлива
        """
        if not {'name'}.issubset(request.data):
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Не указаны все необходимые аргументы'}
            )
        name = request.data.get('name')
        fuel, created = Fuel.objects.get_or_create(name=name,
                                                   photo=request.FILES['file'])
        return JsonResponse({'Status': True})


class ServiceView(APIView):
    """
    Услуга
    """

    @staticmethod
    def get(request, service_id=False, *args, **kwargs):
        """
        Получить информацию по услуге
        """
        if not service_id:
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Необходимо передать id услуги в параметрах запроса'}
            )
        try:
            service = Service.objects.get(id=service_id)
        except GasStation.DoesNotExist:
            return JsonResponse({
                'Status': False,
                'Error': 'Услуги с указанным id не существует'
            })
        service_serializer = ServiceSerializer(service)

        return Response(service_serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Добавить вид услуги
        """
        if not {'name'}.issubset(request.data):
            return JsonResponse(
                {'Status': False,
                 'Errors': 'Не указаны все необходимые аргументы'}
            )
        name = request.data.get('name')
        service, created = Service.objects.get_or_create(name=name,
                                                         photo=request.FILES['file'])
        return JsonResponse({'Status': True})
