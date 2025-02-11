from rest_framework import generics, permissions
from .models import Order
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from orders.permissions import FreelacerPermission
from rest_framework.response import Response



class OrderCreateAPIview(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AcceptedOrderCreateView(APIView):
    permission_classes = [FreelacerPermission]
    serializer_class =  AcceptedOrderSerializer
    
    def perform_create(self, serializer, request, *args, **kwargs):
        #Order instance
        serializer.save(freelcer=self.request.user)
    
class AcceptedOrderDetailedView(APIView):
    queryset = AcceptedOrder.objects.all()
    serializer_class = AcceptedOrderSerializer
    lookup_field = "order.id"
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)