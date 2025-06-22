from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.name

    def current_stock(self):
        stock_in = sum(entry.quantity for entry in self.stock_entries.all())
        stock_out = sum(exit.quantity for exit in self.stock_exits.all())
        adjustments = sum(adj.after - adj.before for adj in self.stock_adjustments.all())
        return stock_in - stock_out + adjustments

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
    quantity = models.IntegerField()  
    transaction_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.product.name} | {self.transaction_type} | {self.quantity} | {self.transaction_date}"

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
