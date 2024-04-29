from django.contrib import admin
from .models import PurchaseOrder
from vendor.models import Vendor, HistoricalPerformance

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'po_number', 'vendor', 'order_date', 'delivery_date',
        'status', 'quality_rating'
    )
    list_filter = ('status', 'vendor')
    search_fields = (
        'po_number', 'vendor__name'
    )  # Allows searching by PO number and vendor name
