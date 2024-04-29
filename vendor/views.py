from rest_framework import generics, permissions, status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Vendor, HistoricalPerformance
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import \
    VendorSerializer, VendorPerformanceSerializer,\
    VendorCreateSerializer, VendorPerformanceDataSerializer

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendorCreateSerializer  # Serializer for creating
        return super().get_serializer_class()


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorCreateSerializer
    lookup_url_kwarg = 'vendor_id'
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_id'
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        historical_performance = None
        from purchaseorder.models import PurchaseOrder
        try:
            latest_completed_order = PurchaseOrder.objects.filter(vendor=vendor, status='completed').latest('order_date')
            historical_performance = HistoricalPerformance.objects.filter(vendor=vendor, date__gt=latest_completed_order.order_date).last()
        except PurchaseOrder.DoesNotExist:
            pass

        if historical_performance:
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        else:
            performance_metrics = vendor.update_performance_metrics()
            serializer = VendorPerformanceDataSerializer(data=performance_metrics)
            if serializer.is_valid():
                serializer.save()
                serializer = VendorPerformanceSerializer(vendor)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcknowledgePurchaseOrderAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, po_id):
        from purchaseorder.models import PurchaseOrder
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({'message': 'Purchase order acknowledged successfully.'})