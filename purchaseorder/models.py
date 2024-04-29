from django.db import models
from django.db.models import Sum
from vendor.models import Vendor
from vendor.models import HistoricalPerformance
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.po_number

@receiver(pre_save, sender=PurchaseOrder)
def update_acknowledgment_date(sender, instance, **kwargs):
    if instance.pk:  # Only update when the instance already exists
        original_instance = PurchaseOrder.objects.get(pk=instance.pk)
        if not original_instance.acknowledgment_date and instance.acknowledgment_date:
            vendor = instance.vendor
            # Calculate Average Response Time
            completed_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
            total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos)
            vendor.average_response_time = total_response_time / completed_pos.count() if completed_pos.count() else 0

            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor

    # Calculate Quality Rating Average
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    vendor.fulfillment_rate = (fulfilled_pos / total_pos) * 100 if total_pos else 0

    if instance.status == 'completed':
        # Calculate On-Time Delivery Rate
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()
        vendor.on_time_delivery_rate = (on_time_deliveries / completed_pos.count()) * 100 if completed_pos.count() else 0

        # Calculate Quality Rating Average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        total_ratings = completed_pos_with_rating.count()
        total_rating_sum = completed_pos_with_rating.aggregate(Sum('quality_rating'))['quality_rating__sum'] or 0
        vendor.quality_rating_avg = total_rating_sum / total_ratings if total_ratings else 0

        # Create HistoricalPerformance instance
        HistoricalPerformance.objects.create(
            vendor=vendor,
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate
        )
    
    vendor.save()
