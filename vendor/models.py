from django.db import models
from django.utils import timezone
from django.db.models import Avg, Count


class Vendor(models.Model):
    name = models.CharField(max_length = 100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length = 50, unique = True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


    def __str__(self):
        return self.name


    def calculate_vendor_performance_metrics(self):
        from purchaseorder.models import PurchaseOrder

        completed_pos = PurchaseOrder.objects.filter(vendor=self, status='completed')
        total_completed_pos = completed_pos.count()

        # Calculate On-Time Delivery Rate
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0

        # Calculate Quality Rating Average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        # Calculate Average Response Time
        completed_pos_with_acknowledgment = completed_pos.exclude(acknowledgment_date__isnull=True)
        total_completed_pos_with_acknowledgment = completed_pos_with_acknowledgment.count()
        total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment)
        average_response_time = total_response_time / total_completed_pos_with_acknowledgment if total_completed_pos_with_acknowledgment > 0 else 0

        # Calculate Fulfillment Rate
        total_pos = PurchaseOrder.objects.filter(vendor=self).count()
        fulfillment_rate = (total_completed_pos / total_pos) * 100 if total_pos > 0 else 0

        return {
            'vendor': self.id,
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate
        }

    def update_performance_metrics(self):
        metrics = self.calculate_vendor_performance_metrics()
        self.on_time_delivery_rate = metrics['on_time_delivery_rate']
        self.quality_rating_avg = metrics['quality_rating_avg']
        self.average_response_time = metrics['average_response_time']
        self.fulfillment_rate = metrics['fulfillment_rate']
        self.save()
        return metrics

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
