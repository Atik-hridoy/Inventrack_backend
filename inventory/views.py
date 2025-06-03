from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Product, ProductModification
from .serializers import ProductSerializer, ProductModificationSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        # Track modification
        ProductModification.objects.create(
            product=instance,
            modified_by=self.request.data.get('modified_by', 'unknown'),  # Replace with user info if available
            change_description=self.request.data.get('change_description', 'Updated product')
        )

    def perform_destroy(self, instance):
        # Track deletion
        ProductModification.objects.create(
            product=instance,
            modified_by=self.request.data.get('modified_by', 'unknown'),
            change_description='Deleted product'
        )
        instance.delete()

class ProductModificationListView(generics.ListAPIView):
    queryset = ProductModification.objects.all()
    serializer_class = ProductModificationSerializer
