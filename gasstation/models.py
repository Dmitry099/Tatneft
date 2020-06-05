from django.db import models
from django.utils.translation import ugettext as _


class GasStation(models.Model):
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lon = models.FloatField(_('Longitude'), blank=True, null=True)
    number = models.PositiveIntegerField(verbose_name='Номер АЗС')
    region = models.CharField(max_length=256, verbose_name='Регион РФ',
                              blank=True, null=True)
    city = models.CharField(max_length=256, verbose_name='Город РФ',
                            blank=True, null=True)
    street = models.CharField(max_length=256, verbose_name='Улица',
                              blank=True, null=True)
    building = models.CharField(max_length=256, verbose_name='Дом',
                                blank=True, null=True)
    zip_code = models.CharField(max_length=6, verbose_name='Индекс',
                                blank=True, null=True)
    fuel = models.ManyToManyField('Fuel', through='FuelStation')
    service = models.ManyToManyField('Service', through='ServiceStation')

    class Meta:
        verbose_name = 'АЗС'
        verbose_name_plural = 'АЗС'

    def __str__(self):
        return str(self.number)


class Fuel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование топлива')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Топливо'
        verbose_name_plural = 'Топливо'

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование услуги')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class FuelStation(models.Model):
    stations = models.ForeignKey(GasStation, on_delete=models.CASCADE,
                                 related_name='fuelstations')
    fuels = models.ForeignKey(Fuel, on_delete=models.CASCADE,
                              related_name='fuels')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Стоимость топлива')
    currency = models.CharField(max_length=50, verbose_name='Валюта')


class ServiceStation(models.Model):
    stations = models.ForeignKey(GasStation, on_delete=models.CASCADE,
                                 related_name='servicestations')
    services = models.ForeignKey(Service, on_delete=models.CASCADE,
                                 related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Стоимость услуги')
