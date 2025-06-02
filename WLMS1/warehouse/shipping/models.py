from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from orders.models import PurchaseOrder
from inventory.models import Product, Warehouse

class Shipment(models.Model):
    SHIPMENT_STATUS = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    shipment_number = models.CharField(max_length=50, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='outgoing_shipments')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='incoming_shipments')
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS, default='pending')
    shipped_date = models.DateField(null=True, blank=True)
    expected_arrival_date = models.DateField(null=True, blank=True)
    actual_arrival_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Shipment-{self.shipment_number}"
    
    def total_items(self):
        return sum(item.quantity for item in self.shipmentitem_set.all())

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product} x {self.quantity}"