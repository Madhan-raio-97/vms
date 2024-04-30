from django.urls import reverse
from django.utils import timezone
from .models import Vendor, HistoricalPerformance
from purchaseorder.models import PurchaseOrder
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            "name": "TDS Technologies",
            "contact_details": "support@tdstech.com",
            "address": "886 Eli Street, Villagetown, US",
            "vendor_code": "VENDOR032"
        }
    
    def test_vendor_create_api_endpoint(self):
        # Replace 'your_endpoint_url' with the actual endpoint URL you want to test
        url = '/api/vendors/'
        
        # Make a request to the API endpoint
        create_response = self.client.post(url, self.data, format='json')
        
        # Assert that the response status code is 200 OK or any other status you expect
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # Assert other conditions based on your API response

    def test_vendor_get_api_endpoint(self):
        # Replace 'your_endpoint_url' with the actual endpoint URL you want to test
        url = '/api/vendors/'
        
        # Make a request to the API endpoint
        response = self.client.get(url)
        
        # Assert that the response status code is 200 OK or any other status you expect
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert other conditions based on your API response

    def test_vendor_retrieve_api_endpoint(self):

        # First, create a vendor using POST method
        create_url = '/api/vendors/'
        create_response = self.client.post(create_url, self.data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Replace 'your_endpoint_url' with the actual endpoint URL you want to test
        retrieve_url = '/api/vendors/{}/'.format(create_response.data['id'])

        
        # Make a request to the API endpoint
        retrieve_response = self.client.get(retrieve_url)
        
        # Assert that the response status code is 200 OK or any other status you expect
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        # Assert other conditions based on your API response
    
    def test_vendor_update_api_endpoint(self):
        create_url = '/api/vendors/'
        create_response = self.client.post(create_url, self.data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        update_data = {
            "name": "New TDS Technologies",
            "contact_details": "new_support@tdstech.com",
            "address": "New Address, New Villagetown, US",
            "vendor_code": "VENDOR032"
        }

        update_url = '/api/vendors/{}/'.format(create_response.data['id'])
        update_response = self.client.put(update_url, update_data, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Add more assertions as needed

    def test_vendor_delete_api_endpoint(self):
        create_url = '/api/vendors/'
        create_response = self.client.post(create_url, self.data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        delete_url = '/api/vendors/{}/'.format(create_response.data['id'])
        delete_response = self.client.delete(delete_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Add more assertions as needed


class VendorPerformanceAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='KDS Technologies', contact_details='support@tdsrtech.com')
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO123",
            order_date=timezone.now() - timezone.timedelta(days=10),
            delivery_date=timezone.now() - timezone.timedelta(days=3),
            quantity=2,
            items=[{"name": "Item1", "quantity": 10}, {"name": "Item2", "quantity": 20}],
            status="completed",
            issue_date=timezone.now() - timezone.timedelta(days=9),
            acknowledgment_date=timezone.now() - timezone.timedelta(days=8)
        )

    def test_get_vendor_performance(self):
        url = reverse('vendor_performance', kwargs={'vendor_id': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(self.vendor.on_time_delivery_rate)
        # print(self.vendor.quality_rating_avg)
        # print(self.vendor.average_response_time)
        # print(self.vendor.fulfillment_rate)
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)
        self.assertEqual(self.vendor.quality_rating_avg, 0)
        self.assertEqual(self.vendor.average_response_time, 0)
        self.assertEqual(self.vendor.fulfillment_rate, 100.0)
