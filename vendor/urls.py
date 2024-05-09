# vendor/urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorRetrieveUpdateDeleteAPIView.as_view(), name='vendor-retrieve-update-delete'),
    
    # API endpoints for Purchase Orders
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDeleteAPIView.as_view(), name='purchase-order-retrieve-update-delete'),
    
    #  status completed in purchase order 
    path('purchase_orders/<int:po_id>/mark_completed/', mark_order_as_completed, name='mark_order_as_completed'),
    
    # vendor performance  
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'),
    
    # Acknowledgment
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name="acknowledge_purchase_order"),


]
