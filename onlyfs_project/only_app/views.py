from only_app.models import Category, Product, Stock, Discount
from rest_framework.generics import ListAPIView
from only_app.serializers import (CategorySerializer, CreatorProductSerializer, ProductCreateSerializer,
                                  ProductBlurredSerializer, StockSerializer)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from only_app.permissions import IsCreatorPermission, IsUserPermission
from only_app.task import some_task


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, )


class CategoryProductsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        some_task.delay()
        serializer = ProductBlurredSerializer(queryset, many=True)
        return Response(serializer.data)


class CreatorOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsCreatorPermission]

    def get(self, request):
        queryset = Product.objects.filter(user=request.user)
        serializer = CreatorProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockListView(ListAPIView):
    permission_classes = (IsAuthenticated, IsUserPermission, )
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
