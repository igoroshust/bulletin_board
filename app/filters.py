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
    # status = ModelChoiceFilter(
    #     field_name='status',
    #     queryset=Response.objects.all(),
    #     label='Отклики',
    # )
    class Meta:
        model = Response
        fields = {
            'status': ['exact'],
        }
