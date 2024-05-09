# vendor/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404


class VendorListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(
            data={"status": status.HTTP_200_OK,"data": serializer.data}
        )

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status": status.HTTP_201_CREATED,"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(  data={
                        "status": status.HTTP_400_BAD_REQUEST, "message": "bad request", "data":serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )


class VendorRetrieveUpdateDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, vendor_id):
        try:
            vendor = self.get_vendor(vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(data={"status": status.HTTP_200_OK, "data": serializer.data})
        except Vendor.DoesNotExist:
            return Response(data={"error": "Vendor not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, vendor_id):
        try:
            vendor = self.get_vendor(vendor_id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status": status.HTTP_200_OK, "data": serializer.data})
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response(data={"error": "Vendor not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, vendor_id):
        try:
            vendor = self.get_vendor(vendor_id)
            vendor.delete()
            return Response(data={"status": status.HTTP_204_NO_CONTENT, "message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response(data={"error": "Vendor not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    def get_vendor(self, vendor_id):
        return Vendor.objects.get(id=vendor_id)


""" Purchase Order """  


class PurchaseOrderListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(data={"status":status.HTTP_200_OK, "data":serializer.data})

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status":status.HTTP_201_CREATED, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"status":status.HTTP_400_BAD_REQUEST, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderRetrieveUpdateDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(data={"status": status.HTTP_404_NOT_FOUND, "message": "data not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(data={"status": status.HTTP_200_OK, "data":serializer.data})

    def put(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(data={"status":status.HTTP_404_NOT_FOUND, "message":"Data not found"},status=status.HTTP_404_NOT_FOUND )

        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status":status.HTTP_200_OK, "data":serializer.data})
        return Response(data={"status":status.HTTP_400_BAD_REQUEST, "data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(data={"status":status.HTTP_404_NOT_FOUND, "message":"Data not found"},status=status.HTTP_404_NOT_FOUND)

        purchase_order.delete()
        return Response(data={"status":status.HTTP_204_NO_CONTENT, "message":"Delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_order_as_completed(request, po_id):
    try:
        order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(data={'message': 'Purchase Order not found', "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_404_NOT_FOUND)

    if order.status == 'completed':
        return Response(data={'message': 'Purchase Order is already marked as completed', "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Mark the order as completed
    order.status = 'completed'
    order.save()

    # Update performance metrics
    order.vendor.update_performance_metrics()

    return Response(data={'message': 'Purchase Order marked as completed', "status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    print("vendor performance")
    # Retrieve the vendor instance
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Retrieve the latest historical performance record or create a new one
    historical_performance = HistoricalPerformance.objects.filter(vendor=vendor).first()

    if not historical_performance:
        # If the historical performance record doesn't exist, return a custom message
        return Response(data={"message": "Historical performance record does not exist for this vendor.", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Serialize the performance data
    serializer = HistoricalPerformanceSerializer(historical_performance)

    return Response(data={"message":"success", "data":serializer.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    # Retrieve the purchase order instance
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    # Check if the purchase order has already been acknowledged
    if purchase_order.acknowledgment_date:
        return Response(data={'message': 'Purchase Order has already been acknowledged', "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Update the acknowledgment_date field
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()

    # Trigger recalculation of average_response_time
    purchase_order.vendor.update_performance_metrics()

    return Response({'message': 'Purchase Order acknowledged successfully', "status":status.HTTP_200_OK}, status=status.HTTP_200_OK)