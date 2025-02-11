from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('token')


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new User.
    Email, Username, and password are required.
    Returns a JSON web token.
    """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'password', 'token',
                  'is_superuser', 'is_gold_member')

    def create(self, validated_data):
        return BaseUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }

class FreelaceSerializer(serializers.Serializer):
    class Meta:
        model = Freelancer
        fields = '__all__'
        
class CustomSerializer(serializers.Serializer):
    class Meta:
        model = Customer
        fields = '__all__'

class RivewCFSerializer(serializers.Serializer):
    class Meta:
        model = ReviewCF
        fields = '__all__'

class RivewFCSerializer(serializers.Serializer):
    class Meta:
        model = ReviewFC
        fields = '__all__'