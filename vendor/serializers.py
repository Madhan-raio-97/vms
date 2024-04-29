from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):

    # Override the on_time_delivery_rate field to make it optional with a default value
    on_time_delivery_rate = serializers.FloatField(default=0)
    quality_rating_avg = serializers.FloatField(default=0)
    average_response_time = serializers.FloatField(default=0)
    fulfillment_rate = serializers.FloatField(default=0)

    class Meta:
        model = Vendor
        fields = '__all__'

class VendorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
