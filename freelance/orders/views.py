from rest_framework import generics, permissions
from .models import Order
from .serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderCreateAPIview(generics.CreateView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)

        if status:
            queryset = queryset.filter(status=status)

        if getattr(user, 'is_freelancer', False):
            return queryset.filter(freelancer=user)

        return queryset.filter(client=user)
