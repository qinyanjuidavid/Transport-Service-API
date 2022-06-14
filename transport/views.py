from transport.serializers import ProviderSerializer, ServiceAreaSerializer
from transport.models import Provider, ServiceArea
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.gis.geos import GEOSGeometry, Point


class ProviderAPIView(ModelViewSet):
    serializer_class = ProviderSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'post',
                         'put', 'delete']

    def get_queryset(self):
        providerObj = Provider.objects.all()
        return providerObj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(
            {'message': 'Provider deleted successfully'},
            status=status.HTTP_204_NO_CONTENT)


class ServiceAreaAPIView(ModelViewSet):
    serializer_class = ServiceAreaSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        serviceAreaQs = ServiceArea.objects.all()
        return serviceAreaQs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(
            {'message': 'Service Area deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_name="get_service_area")
    def filterServiceArea(self, request):
        lat = request.query_params.get('lat', None)
        lng = request.query_params.get('lng', None)
        # If lat and lng are not Null
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            point = Point(lat, lng, srid=4326)
            serviceArea = ServiceArea.objects.filter(
                geom__contains=point)
            print(serviceArea)
            # Check is the point provided is in any service area
            if serviceArea.exists():
                serializer = self.get_serializer(serviceArea, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # If point not available notify the user
            else:
                return Response(
                    {'message': 'The latitude and longitude  provided is not in any service area.'},
                    status=status.HTTP_200_OK
                )
        # Else we return a message requesting for lat and lng
        return Response(
            {'message': 'Please provide latitude and longitude'},
            status=status.HTTP_400_BAD_REQUEST
        )
