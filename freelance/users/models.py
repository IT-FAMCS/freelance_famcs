from datetime import datetime, timedelta
import jwt
from users.choises.service_choises import SERVICE_EN
from django.core import validators
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
    )
    is_staff = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_gold_member = models.BooleanField(default=False)
    telegram = models.TextField(blank=True)
    watsup = models.TextField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp()),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    @property
    def token(self):
        return self._generate_jwt_token()
    
    
class Freelancer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=50)
    services_sector = models.TextField(choices=SERVICE_EN)
    rating = models.FloatField(max_length=3)
    resume = models.TextField(blank=True)
    def __str__(self):
        return self.user.username

    
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=50)
    rating = models.FloatField(max_length=3)
    def __str__(self):
        return self.user.username
    
class ReviewCF(models.Model):
    reviewer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recepient = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    text = models.TextField(default="")
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.recepient.user.username}: {self.rating}"
class ReviewFC(models.Model):
    reviewer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    recepient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.TextField(default="")
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.recepient.user.username}: {self.rating}"