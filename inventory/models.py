from django.db import models
from django.conf import settings


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text='Discount percentage (e.g. 10 for 10%)')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('other', 'Other'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('sports', 'Sports'),
        ('automotive', 'Automotive'),
        ('health', 'Health'),
        ('beauty', 'Beauty'),
        ('garden', 'Garden'),
        ('computers', 'Computers'),
        ('jewelry', 'Jewelry'),
        ('musical_instruments', 'Musical Instruments'),
        ('office_products', 'Office Products'),
        ('pet_supplies', 'Pet Supplies'),
        ('tools', 'Tools'),
        ('video_games', 'Video Games'),
        ('baby', 'Baby'),
        ('groceries', 'Groceries'),
        ('furniture', 'Furniture'),
        ('appliances', 'Appliances'),
        ('clothing_shoes', 'Clothing & Shoes'),
        ('bags', 'Bags'),
        ('accessories', 'Accessories'),
        ('watches', 'Watches'),
        ('phones', 'Phones'),
        ('tablets', 'Tablets'),
        ('cameras', 'Cameras'),
        ('drones', 'Drones'),
        # Add more as needed
    ]
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name

    def current_stock(self):
        stock_in = sum(entry.quantity for entry in self.stock_entries.all())
        stock_out = sum(exit.quantity for exit in self.stock_exits.all())
        adjustments = sum(adj.after - adj.before for adj in self.stock_adjustments.all())
        return stock_in - stock_out + adjustments

    def total_value(self):
        total = self.current_stock() * self.price
        discount = 0
        coupon_code = None
        if self.coupon and self.coupon.active:
            discount = (total * self.coupon.discount_percent) / 100
            coupon_code = self.coupon.code
        return {
            'total': float(total),
            'discount': float(discount),
            'final_total': float(total - discount),
            'coupon_code': coupon_code
        }

class ProductModification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='modifications')
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)  # Or use ForeignKey to User if you have authentication
    change_description = models.TextField()

    def __str__(self):
        return f"{self.product.name} modified at {self.modified_at}"
    


class StockManagement(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
        ('correction', 'Correction'),
    ]

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()  # Positive for in, negative for out, diff for adjust
    transaction_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    price_at_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set price and discount info at transaction time
        if not self.price_at_transaction:
            self.price_at_transaction = self.product.price
        self.total_value = abs(self.quantity) * self.price_at_transaction
        if self.product.coupon and self.product.coupon.active:
            self.coupon_code = self.product.coupon.code
            self.discount_percent = self.product.coupon.discount_percent
            self.discount_amount = (self.total_value * self.discount_percent) / 100
        else:
            self.discount_amount = 0
        self.final_value = self.total_value - (self.discount_amount or 0)
        # Standard business logic for stock management
        if self.transaction_type == 'in' and self.quantity <= 0:
            raise ValueError('Stock In quantity must be positive.')
        if self.transaction_type == 'out' and self.quantity >= 0:
            raise ValueError('Stock Out quantity must be negative.')
        if self.transaction_type == 'out':
            current_stock = self.product.current_stock()
            if current_stock + self.quantity < 0:
                raise ValueError('Not enough stock to complete this operation.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} | {self.transaction_type} | {self.quantity} | {self.transaction_date} | {self.final_value}"

class StockEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_entries')
    quantity = models.PositiveIntegerField()
    entry_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    def __str__(self):
        return f"{self.product.name} | IN | {self.quantity} | {self.entry_date}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from .models import StockManagement
            StockManagement.objects.create(
                product=self.product,
                transaction_type='in',
                quantity=self.quantity,
                note=self.reason,
                performed_by=self.performed_by,
                transaction_date=self.entry_date
            )

class StockExit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_exits')
    quantity = models.PositiveIntegerField()
    exit_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    def __str__(self):
        return f"{self.product.name} | OUT | {self.quantity} | {self.exit_date}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from .models import StockManagement
            StockManagement.objects.create(
                product=self.product,
                transaction_type='out',
                quantity=-self.quantity,  # negative for out
                note=self.reason,
                performed_by=self.performed_by,
                transaction_date=self.exit_date
            )

class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_adjustments')
    before = models.IntegerField()
    after = models.IntegerField()
    adjustment_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    def __str__(self):
        return f"{self.product.name} | ADJUST | {self.before}→{self.after} | {self.adjustment_date}"
