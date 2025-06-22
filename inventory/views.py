from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Product, ProductModification, StockEntry, StockExit, StockAdjustment
from .serializers import ProductSerializer, ProductModificationSerializer


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'role') and request.user.role == 'staff')

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

class StockEntryCreateView(APIView):
    permission_classes = [IsStaffUser]  # Allow any user to add stock (customize as needed)
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', '')
        performed_by = request.data.get('performed_by')  # Optional: user id
        if not product_id or not quantity:
            return Response({'error': 'product_id and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        entry = StockEntry.objects.create(
            product=product,
            quantity=quantity,
            reason=reason,
            performed_by_id=performed_by
        )
        return Response({'message': 'Stock added successfully.', 'entry_id': entry.id}, status=status.HTTP_201_CREATED)

class StockExitCreateView(APIView):
    permission_classes = [IsStaffUser]  # Allow any user to remove stock (customize as needed)
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', '')
        performed_by = request.data.get('performed_by')  # Optional: user id
        if not product_id or not quantity:
            return Response({'error': 'product_id and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        exit = StockExit.objects.create(
            product=product,
            quantity=quantity,
            reason=reason,
            performed_by_id=performed_by
        )
        return Response({'message': 'Stock removed successfully.', 'exit_id': exit.id}, status=status.HTTP_201_CREATED)

class StockMovementLogView(APIView):
    permission_classes = [IsStaffUser]
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        entries = product.stock_entries.all()
        exits = product.stock_exits.all()
        adjustments = product.stock_adjustments.all()
        log = []
        for entry in entries:
            log.append({
                'type': 'in',
                'quantity': entry.quantity,
                'date': entry.entry_date,
                'reason': entry.reason,
                'performed_by': entry.performed_by_id
            })
        for exit in exits:
            log.append({
                'type': 'out',
                'quantity': exit.quantity,
                'date': exit.exit_date,
                'reason': exit.reason,
                'performed_by': exit.performed_by_id
            })
        for adj in adjustments:
            log.append({
                'type': 'adjust',
                'before': adj.before,
                'after': adj.after,
                'date': adj.adjustment_date,
                'reason': adj.reason,
                'performed_by': adj.performed_by_id
            })
        log.sort(key=lambda x: x['date'])
        return Response({'product': product.name, 'log': log}, status=status.HTTP_200_OK)

class ProductListWithStockView(APIView):
    permission_classes = [IsStaffUser]
    def get(self, request):
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'current_stock': product.current_stock(),
                'price': str(product.price),
                'category': product.category
            })
        return Response(data, status=status.HTTP_200_OK)
