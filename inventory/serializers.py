from rest_framework import serializers
from .models import Product, ProductModification

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'quantity', 'price',
            'description', 'image', 'category'
        ]

class ProductModificationSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = ProductModification
        fields = ['id', 'product', 'product_name', 'modified_at', 'modified_by', 'change_description']