from django.urls import path
from .views import ProductCreateView, ProductListView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('list/', ProductListView.as_view(), name='product-list'),
]