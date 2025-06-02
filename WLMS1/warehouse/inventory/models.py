from django.db import models
import uuid

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)  # Make SKU optional
    description = models.TextField(blank=True)  # Optional
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    # ... other fields ...

    def save(self, *args, **kwargs):
        if not self.sku:  # Auto-generate SKU if empty
            self.sku = f"PROD-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
    upc = models.CharField(max_length=50, unique=True, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=20)
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True,  # Allows empty form submission
        null=True,   # Allows NULL in database
        default=0.0, # Optional: set default value
        help_text="Weight in kg (optional)"
    )
    volume = models.DecimalField(max_digits=10, decimal_places=2, help_text="Volume in cubic meters")
    reorder_level = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_allocated = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'warehouse')
        verbose_name_plural = "Inventory"
    
    def __str__(self):
        return f"{self.product} at {self.warehouse} - {self.quantity_on_hand} units"
    
    @property
    def available_quantity(self):
        return self.quantity_on_hand - self.quantity_allocated