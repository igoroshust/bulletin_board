from django_filters import FilterSet
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
