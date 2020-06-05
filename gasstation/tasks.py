import configparser
import requests

from Tatneft.celery import celery_app
from .models import GasStation
from .models import Service
from .models import Fuel

config = configparser.ConfigParser()
config.read("sources.conf")

url_first_path = config['source']['url_first_path']
url_second_path = config['source']['url_second_path']


@celery_app.task
def get_first_source_info():
        """
        Периодическая задача на получение информации с первого
        источника
        """
        if url_first_path:
            headers = {
                "Accept": "application/json",
                "Accept-language": "ru",
                "Content-Type": "application/json"
            }

            response = requests.get(url_first_path, headers=headers)
            gas_stations_info = response.json()['response']
            for gas_station in gas_stations_info:
                id = gas_station.get('id')
                lat = gas_station.get('lat')
                lon = gas_station.get('lon')
                number = gas_station.get('number')
                region = gas_station.get('region')
                city = gas_station.get('city')
                street = gas_station.get('street')
                building = gas_station.get('building')
                zip_code = gas_station.get('zip_code')
                photos = gas_station.get('photos')
                services = gas_station.get('services')
                gas_station, created = GasStation.objects.get_or_create(id=id)
                gas_station.lat = lat
                gas_station.lon = lon
                gas_station.number = number
                gas_station.region = region
                gas_station.city = city
                gas_station.street = street
                gas_station.building = building
                gas_station.zip_code = zip_code
                gas_station.save()
                for type, type_id, photo in photos:
                    if type == 'service':
                        service, created = Service.objects.get_or_create(
                            id=type_id
                        )
                        service.image = photo
                        service.save()
                    else:
                        fuel, created = Fuel.objects.get_or_create(
                            id=type_id
                        )
                        fuel.image = photo
                        fuel.save()
                for service_id, service_name in services:
                    service, created = Service.objects.get_or_create(
                        id=service_id
                    )
                    service.name = service_name
                    service.save()


@celery_app.task
def get_second_source_info():
        """
        Периодическая задача на получение информации с первого
        источника
        """
        if url_second_path:
            headers = {
                "Accept": "application/json",
                "Accept-language": "ru",
                "Content-Type": "application/json"
            }

            response = requests.get(url_second_path, headers=headers)
            gas_stations_info = response.json()['response']
            for gas_station in gas_stations_info:
                id = gas_station.get('id')
                prices = gas_station.get('prices')
                gas_station, created = GasStation.objects.get_or_create(id=id)
                for name, price, currency in prices:
                    fuel, created = Fuel.objects.get_or_create(
                        name=name,
                        price=price,
                        currency=currency
                    )
                    gas_station.fuel.add(fuel)
                gas_station.save()
