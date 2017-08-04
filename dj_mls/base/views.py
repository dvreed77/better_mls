from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import pagination
# import django_filters.rest_framework
from django_filters import rest_framework as filters
import django_filters
# from url_filter.backends.django import DjangoFilterBackend
# from url_filter.integrations.drf import DjangoFilterBackend

from .serializers import *
from .models import *
from rest_framework import permissions


class MLSListingFilter(filters.FilterSet):
    start_date = django_filters.DateTimeFilter(name="created", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(name="created", lookup_expr='lte')
    max_beds = django_filters.NumberFilter(name="n_beds", lookup_expr='lte')
    min_living_area = django_filters.NumberFilter(name="living_area", lookup_expr='gte')
    max_living_area = django_filters.NumberFilter(name="living_area", lookup_expr='lte')
    min_walking_duration = django_filters.NumberFilter(name="walking_duration", lookup_expr='gte')
    max_walking_duration = django_filters.NumberFilter(name="walking_duration", lookup_expr='lte')

    class Meta:
        model = MLSListing
        fields = [
            'start_date',
            'end_date',
            'max_beds',
            'min_living_area',
            'max_living_area',
            'min_walking_duration',
            'max_walking_duration'
            ]


class MLSListingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MLSListingSerializer
    queryset = MLSListing.objects.all()
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ['n_beds', 'walking_duration']
    filter_class = MLSListingFilter

class MLSPriceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MLSPriceSerializer
    queryset = MLSPrice.objects.all()
