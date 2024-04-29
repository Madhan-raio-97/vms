from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Vendor
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import VendorSerializer, VendorPerformanceSerializer, VendorCreateSerializer

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

class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({'message': 'Purchase order acknowledged successfully.'})