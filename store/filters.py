from django_filters import FilterSet
from django_filters import rest_framework as filters
from .models import Store


class StoreFilter(FilterSet):
    """
    Create a filter class that inherits from FilterSet. This class will help
    us search for store using specified fields.
    """
    product = filters.CharFilter(lookup_expr='icontains')
    variation = filters.CharFilter(lookup_expr='icontains')
    origin = filters.CharFilter(lookup_expr='icontains')
    price = filters.RangeFilter()
  


    class Meta:
        model = Store
        fields = (
            'product',
            'variation',
            'origin',
            'price',
        )