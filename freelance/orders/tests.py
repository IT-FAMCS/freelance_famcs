from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username='client', email='client@example.com', password='password123')
        # Имя URL, где расположен ListCreateAPIView для заказов
        self.url = reverse('order-list-create')

    def test_create_order(self):
        self.client.login(username='client@example.com',
                          password='password123')  # Логинимся
        data = {
            "title": "Test Order",
            "description": "Test order description",
            "price": "150.00",
            "deadline": "2024-12-31T00:00:00Z"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
