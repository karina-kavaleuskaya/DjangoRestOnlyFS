from django.urls import path
from only_app.views import (CategoryListView, CategoryProductsView, CreatorOnlyView,
                            StockListView)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category-product'),
    path('my_store/', CreatorOnlyView.as_view(), name='my-store'),
    path('stock/', StockListView.as_view(), name='stock'),
]