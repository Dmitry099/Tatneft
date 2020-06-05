from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import GasStation, Fuel, Service, FuelStation, ServiceStation


class FuelStationInline(admin.TabularInline):
    model = FuelStation
    extra = 1


class ServiceStationInline(admin.TabularInline):
    model = ServiceStation
    extra = 1


@admin.register(GasStation)
class GasStationAdmin(admin.ModelAdmin):
    inlines = [FuelStationInline, ServiceStationInline]


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
