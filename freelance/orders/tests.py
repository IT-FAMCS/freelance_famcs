from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.client_user = User.objects.create_user(
            username='client', email='client@example.com', password='password123'
        )
        # Имя URL, где расположен ListCreateAPIView для заказов
        self.url = reverse('order-list-create')

    def test_create_order(self):
        # Логинимся и добавляем логирование
        logger.info('Logging in as client...')
        login_successful = self.client.login(
            username='client@example.com', password='password123')
        if login_successful:
            logger.info('Login successful.')
        else:
            logger.error('Login failed.')

        # Логируем отправляемые данные
        data = {
            "title": "Test Order",
            "description": "Test order description",
            "price": "150.00",
            "deadline": "2024-12-31T00:00:00Z",
            "client": self.client_user.id  # Передаем ID клиента
        }
        logger.info(
            'Sending POST request to create an order with data: %s', data)

        # Отправка POST-запроса
        response = self.client.post(self.url, data, format='json')

        # Логируем результат
        logger.info('Received response: %s', response.content)
        logger.info('Response status code: %s', response.status_code)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        # Логинимся и добавляем логирование
        logger.info('Logging in as client...')
        login_successful = self.client.login(
            username='client@example.com', password='password123')
        if login_successful:
            logger.info('Login successful.')
        else:
            logger.error('Login failed.')

        # Логируем запрос на получение заказов
        logger.info('Sending GET request to retrieve orders.')

        # Отправка GET-запроса
        response = self.client.get(self.url)

        # Логируем результат
        logger.info('Received response: %s', response.content)
        logger.info('Response status code: %s', response.status_code)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
