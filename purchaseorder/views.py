from rest_framework import permissions
from rest_framework.generics import \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import \
    TokenAuthentication, SessionAuthentication
from .models import PurchaseOrder, Vendor
from .serializers import \
    PurchaseOrderSerializer, PurchaseOrderCreateSerializer


class PurchaseOrderListCreateAPIView(ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseOrderCreateSerializer  # Serializer for creating
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id = vendor_id)
        return queryset


class PurchaseOrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderCreateSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
