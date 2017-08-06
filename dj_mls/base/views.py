from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import pagination
from django_filters import rest_framework as filters
import django_filters
from django.db.models import Q

from .serializers import *
from .models import *
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta

def is_active(queryset, name, value):
    return queryset.filter(~Q(current_status = 'CTG'))

def is_recent(queryset, name, value):
    return queryset.filter(latest_update__gte=timezone.now()-timedelta(days=int(value)))

class MLSCompleteFilter(filters.FilterSet):
    start_date = django_filters.DateTimeFilter(name="created", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(name="created", lookup_expr='lte')
    max_beds = django_filters.NumberFilter(name="n_beds", lookup_expr='lte')
    min_living_area = django_filters.NumberFilter(name="living_area", lookup_expr='gte')
    max_living_area = django_filters.NumberFilter(name="living_area", lookup_expr='lte')
    min_walking_duration = django_filters.NumberFilter(name="walking_duration", lookup_expr='gte')
    max_walking_duration = django_filters.NumberFilter(name="walking_duration", lookup_expr='lte')
    active = django_filters.BooleanFilter(name="current_status", method=is_active)
    recent = django_filters.NumberFilter(name="latest_update", method=is_recent)
    max_price = django_filters.NumberFilter(name="current_price", lookup_expr='lte')

    class Meta:
        model = MLSComplete
        fields = [
            'start_date',
            'end_date',
            'max_beds',
            'min_living_area',
            'max_living_area',
            'min_walking_duration',
            'max_walking_duration',
            'active',
            'recent',
            'max_price'
            ]


class MLSCompleteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MLSCompleteSerializer
    queryset = MLSComplete.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MLSCompleteFilter
