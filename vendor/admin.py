from django.contrib import admin
from .models import Vendor, HistoricalPerformance

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'vendor_code', 'on_time_delivery_rate',
        'quality_rating_avg', 'average_response_time', 'fulfillment_rate'
    )
    # Add more customization as needed

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'vendor', 'date', 'on_time_delivery_rate',
        'quality_rating_avg', 'average_response_time', 'fulfillment_rate'
    )
    list_filter = ('vendor', 'date')
    # Add more customization as needed
