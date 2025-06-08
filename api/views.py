from django.db.models import Max
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, OrderCreateSerializer
from api.models import Product, Order, OrderItem
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from api.filters import OrderFilter, ProductFilter, InStockFilterBackend

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

def home(request):
    return render(request, 'base.html')

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter, 
        InStockFilterBackend
    ]
    search_fields = ['=name', 'desc']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 4

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

# @api_view(['GET'])
# def order_list(request):
#     #added prefetch_related to optimize the query; optimized using silk package
#     orders = Order.objects.prefetch_related('items__product', 'user')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product', 'user')
#     serializer_class = OrderSerializer

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product', 'user')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })

#     return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(
        detail=False,
        methods=['GET'],
        url_path='user-orders'
    )
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)