from rest_framework import serializers
from .models import \
    Vendor, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class VendorPerformanceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

