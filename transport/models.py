from locale import currency
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.validators import UnicodeUsernameValidator
# from languages.fields import LanguageField
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models as gis_models


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Provider(TrackingModel):
    name = models.CharField(
        _('name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': ('A user with that email already exists.'),
    })
    phone = PhoneNumberField(
        _('phone number'), unique=True,
        blank=True, null=True, max_length=27)
    language = models.CharField(_("language"), blank=True, max_length=40,
                                null=True)
    # language=LanguageField(_('language'), blank=True, null=True)
    # currency = MoneyField(
    #     max_digits=10, decimal_places=2,
    #     null=True,
    #     default_currency=None)
    currency = models.CharField(
        _('currency'), max_length=57,
        default="USD")

    class Meta:
        verbose_name = 'provider'
        verbose_name_plural = 'providers'
        ordering = ["-id", ]

    def __str__(self):
        return self.name


class ServiceArea(TrackingModel):
    # Assuming that one Service area has one provider
    provider = models.OneToOneField(Provider,
                                    on_delete=models.DO_NOTHING,)
    name = models.CharField(_('name of service area'),
                            max_length=150, unique=True)
    price = models.FloatField(_('price'), default=0.00)
    geom = gis_models.MultiPolygonField(blank=True, null=True)

    class Meta:
        verbose_name = 'service area'
        verbose_name_plural = 'service areas'
        ordering = ["-id", ]

    def __str__(self):
        return self.name
