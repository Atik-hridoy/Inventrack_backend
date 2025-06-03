from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class ProductModification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='modifications')
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100)  # Or use ForeignKey to User if you have authentication
    change_description = models.TextField()

    def __str__(self):
        return f"{self.product.name} modified at {self.modified_at}"