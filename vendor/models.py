from django.db import models
from django.utils import timezone

# Create your models here.

""" vendor model"""
# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=30,null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=30, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, default=0.0)
    quality_rating_avg = models.FloatField(null=True, default=0.0)
    average_response_time = models.FloatField(null=True, default=0.0)
    fulfillment_rate = models.FloatField(null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    def update_performance_metrics(self):
        # Retrieve or create the latest historical performance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=self, date=timezone.now())

        # Update on-time delivery rate
        completed_orders = self.purchaseorder_set.filter(status='completed', delivery_date__lte=models.F('acknowledgment_date'))
        total_completed_orders = completed_orders.count()
        historical_performance.on_time_delivery_rate = (total_completed_orders / self.purchaseorder_set.filter(status='completed').count()) * 100 if total_completed_orders > 0 else 0

        # Update quality rating average
        completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
        historical_performance.quality_rating_avg = completed_orders_with_rating.aggregate(avg_quality_rating=models.Avg('quality_rating'))['avg_quality_rating'] or 0

        # Update average response time
        acknowledged_orders = completed_orders.filter(acknowledgment_date__isnull=False)
        avg_response_time = acknowledged_orders.aggregate(avg_response_time=models.Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_response_time']
        historical_performance.average_response_time = avg_response_time.total_seconds() if avg_response_time else 0

        # Update fulfillment rate
        total_orders = self.purchaseorder_set.all()
        fulfilled_orders = total_orders.filter(status='completed', issue_date__isnull=False)
        historical_performance.fulfillment_rate = (fulfilled_orders.count() / total_orders.count()) * 100 if total_orders.count() > 0 else 0

        # Save the updated metrics to historical performance
        historical_performance.save()
        
        
"""Purchase order"""
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(default=0,null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='Pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"PO: {self.po_number} - Vendor: {self.vendor.name} - Status: {self.status}"
    
    
""" Historical Performance """
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True,default=0.0)
    quality_rating_avg = models.FloatField(null=True, default=0.0)
    average_response_time = models.FloatField(null=True, default=0.0)
    fulfillment_rate = models.FloatField(null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Performance Record for {self.vendor.name} on {self.date}"    
    
    
 