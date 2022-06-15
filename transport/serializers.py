from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from transport.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name',
                  'email', 'phone',
                  'language', 'currency',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at',
                            'updated_at')


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = ServiceArea
        fields = ('id',  'provider',
                  'name', 'price', 'geom',
                  'created_at', 'updated_at')
        geo_field = 'geom'
        read_only_fields = ('id', 'created_at',
                            'updated_at')
