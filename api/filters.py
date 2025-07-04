import django_filters
from api.models import Order, Product
from rest_framework.filters import BaseFilterBackend

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range']
        }

class InStockFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt = 0)

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        }