from django.urls import path

from .views import GasStationView
from .views import GasStationsView
from .views import FuelStationView
from .views import ServiceStationView
from .views import FuelsView
from .views import FuelView
from .views import ServicesView
from .views import ServiceView


gas_stations_list = GasStationsView.as_view({'get': 'list'})
fuels_list = FuelsView.as_view({'get': 'list'})
services_list = ServicesView.as_view({'get': 'list'})

app_name = 'main'

urlpatterns = [
    path('gasstations/', gas_stations_list, name='gasstations'),
    path('fuels/', fuels_list, name='fuels'),
    path('fuel/<int:fuel_id>/', FuelView.as_view(), name='fuel'),
    path('services/', services_list, name='services'),
    path('service/<int:service_id>/', ServiceView.as_view(), name='service'),
    path('gasstation/<int:station_id>/', GasStationView.as_view(),
         name='gasstation'),
    path('fuelsstation/<int:station_id>/', FuelStationView.as_view(),
         name='fuelsstation'),
    path('servicesstation/<int:station_id>/', ServiceStationView.as_view(),
         name='servicesstation'),
]
