from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserAPIView, VerifyTokenView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token-list/', UserAPIView.as_view(), name='list'),
    path('verify_token/', VerifyTokenView.as_view(), name='verify_token'),
]
