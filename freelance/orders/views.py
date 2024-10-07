from rest_framework import generics, permissions
from .models import Order
from .serializer import OrderSerializer, CreateOrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Клиенты могут просматривать свои заказы, фрилансеры - свои назначенные заказы
        if self.request.user.is_freelancer:
            return self.queryset.filter(freelancer=self.request.user)
        return self.queryset.filter(client=self.request.user)
