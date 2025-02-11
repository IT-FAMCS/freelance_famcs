from django.urls import path
from .views import OrderDetailView

urlpatterns = [
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
