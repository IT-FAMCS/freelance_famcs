from django.db import models
from django.conf import settings
from users.models import Customer, Freelancer


class Order(models.Model):
    client = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='client_orders',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('complited', 'Complited'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    complited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class AcceptedOrder(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="accepted-order"
        )
    freelancer = models.ForeignKey(
        Freelancer, 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return self.order.title