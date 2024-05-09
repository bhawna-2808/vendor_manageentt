from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Vendor)
class AdminVendor(admin.ModelAdmin):
    list_display=('name', 'vendor_code')
    
    
@admin.register(PurchaseOrder)
class AdminPurchaseOrder(admin.ModelAdmin):
    list_display=('po_number', 'quantity')    
    

@admin.register(HistoricalPerformance)
class AdminHistoricalPerformance(admin.ModelAdmin):
    list_display=('vendor', 'quality_rating_avg')              