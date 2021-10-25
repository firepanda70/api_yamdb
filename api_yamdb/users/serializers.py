from rest_framework import serializers, validators

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=(
                                       validators.UniqueValidator(
                                           queryset=User.objects.all()
                                       ),
                                   ))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role', 'email')


class UserAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=(
                                       validators.UniqueValidator(
                                           queryset=User.objects.all()
                                       ),
                                   ))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.SlugField(required=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)
