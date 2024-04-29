from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import PurchaseOrder, Vendor
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='TDS Technologies', contact_details='support@tdstech.com')
        self.po_data = {
            "po_number": "PO123",
            "vendor": self.vendor,
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=7),
            "items": '[{"name": "Item1", "quantity": 10}, {"name": "Item2", "quantity": 20}]',
            "quantity": 2,
            "status": "pending",
            "quality_rating": 3.5,
            "issue_date": timezone.now()
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

    def test_get_purchase_order_list(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')
        updated_data = self.po_data.copy()
        updated_data['po_number'] = "PO124"
        updated_data['vendor'] = self.vendor.pk
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        updated_data = self.po_data.copy()
        updated_data['vendor'] = self.vendor.pk
        updated_data['delivery_date'] = timezone.now() + timezone.timedelta(days=14)
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AcknowledgePurchaseOrderAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='TDS Technologies', contact_details='support@tdstech.com')
        self.po_data = {
            "po_number": "PO123",
            "vendor": self.vendor,
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=7),
            "items": '[{"name": "Item1", "quantity": 10}, {"name": "Item2", "quantity": 20}]',
            "quantity": 2,
            "status": "pending",
            "quality_rating": 3.5,
            "issue_date": timezone.now()
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge_purchase_order', kwargs={'po_id': self.po.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertIsNotNone(self.po.acknowledgment_date)
        self.assertEqual(response.data, {'message': 'Purchase order acknowledged successfully.'})
