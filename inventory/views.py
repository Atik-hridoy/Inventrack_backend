from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductModification
from .serializers import ProductSerializer, ProductModificationSerializer


class ProductListCreateView(APIView):
    permission_classes = []  # Anyone can create a product
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        category = request.query_params.get('category')
        if category:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ProductModification.objects.create(
                product=instance,
                modified_by=request.data.get('modified_by', 'unknown'),
                change_description=request.data.get('change_description', 'Updated product')
            )
            return Response(ProductSerializer(instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            ProductModification.objects.create(
                product=instance,
                modified_by=request.data.get('modified_by', 'unknown'),
                change_description=request.data.get('change_description', 'Partially updated product')
            )
            return Response(ProductSerializer(instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        ProductModification.objects.create(
            product=product,
            modified_by=request.data.get('modified_by', 'unknown'),
            change_description='Deleted product'
        )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductModificationListView(APIView):
    def get(self, request):
        modifications = ProductModification.objects.all()
        serializer = ProductModificationSerializer(modifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GroupedProductFeedView(APIView):
    def get(self, request):
        grouped = {}
        for cat, _ in Product.CATEGORY_CHOICES:
            products = Product.objects.filter(category=cat)
            serializer = ProductSerializer(products, many=True)
            grouped[cat] = serializer.data
        return Response({"success": True, "data": grouped}, status=status.HTTP_200_OK)
