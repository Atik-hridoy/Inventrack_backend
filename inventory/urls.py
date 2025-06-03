from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductModificationListView
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('modifications/', ProductModificationListView.as_view(), name='product-modification-list'),
]
