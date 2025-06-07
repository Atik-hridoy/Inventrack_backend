from django.db import models

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

class ProductModification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='modifications')
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)  # Or use ForeignKey to User if you have authentication
    change_description = models.TextField()

    def __str__(self):
        return f"{self.product.name} modified at {self.modified_at}"