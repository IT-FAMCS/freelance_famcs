from rest_framework import serializers
from .models import Order, AcceptedOrder


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
class AcceptedOrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AcceptedOrder
        fields = '__all__'