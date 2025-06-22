from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductModificationListView,
    StockEntryCreateView,
    StockExitCreateView,
    StockMovementLogView,
    ProductListWithStockView,
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('modifications/', ProductModificationListView.as_view(), name='product-modification-list'),
    path('stock-in/', StockEntryCreateView.as_view(), name='stock-entry-create'),
    path('stock-out/', StockExitCreateView.as_view(), name='stock-exit-create'),
    path('stock-log/<int:product_id>/', StockMovementLogView.as_view(), name='stock-movement-log'),
    path('with-stock/', ProductListWithStockView.as_view(), name='product-list-with-stock'),
]
