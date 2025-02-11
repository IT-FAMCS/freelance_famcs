from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
import jwt
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models

from users.models import BaseUser
from users.serializer import *
from users.serializer import RegistrationSerializer, UserSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None)
            },
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class VerifyTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data.get('token', None)

        if token is None:  # если токен не передан
            return Response(
                {'error': 'Token must be included in the request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except ExpiredSignatureError:  # если токен просрочен
            return Response(
                {'error': 'Token is expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidTokenError:  # если токен невалиден
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateFreelancer(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FreelaceSerializer

    def post(self, request, *args):
        self.create(request,user=self.request.user, *args)

class CreateCustomer(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomSerializer

    def post(self, request, *args):
        self.create(request,user=self.request.user, *args)

class RivewCFCreate(APIView):
    permission_classes = (AllowAny,) #Dev
    serializer_class = RivewCFSerializer

    def post(self, request, *args):
        self.create(request, customer=self.request.user, *args)

class RivewFCCreate(APIView):
    permission_classes = (AllowAny,) #Dev
    serializer_class = RivewFCSerializer

    def post(self, request, *args):
        self.create(request, freelancer=self.request.user, *args)