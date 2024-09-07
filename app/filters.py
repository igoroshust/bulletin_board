import django_filters
from django_filters import FilterSet, ModelChoiceFilter
from .models import *

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
        }


class PublicationFilter(FilterSet):
    class Meta:
        model = Publication
        fields = {
            'name': ['icontains'],
        }

class ResponseFilter(django_filters.FilterSet):

    class Meta:
        model = Response
        fields = {
            'status': ['exact'],
        }

