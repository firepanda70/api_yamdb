from api.permissions import IsAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL

from .serializers import (ConfirmationCodeSerializer, TokenSerializer,
                          UserAdminSerializer, UserSerializer)

EMAIL_SUBJECT = 'Подтверждение регистрации на YaMDb'
EMAIL_MESSAGE = 'Код подтверждения регистрации:'
USERNAME_ME_CREATE_ERROR_MESSAGE = 'Недопустимый username: me'
USERNAME_ME_PATCH_ERROR_MESSAGE = 'Нельзя поменять себе роль'

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if username == 'me':
            return Response(data={'message': USERNAME_ME_CREATE_ERROR_MESSAGE},
                            status=status.HTTP_400_BAD_REQUEST)
        if (
                User.objects.filter(email=email).exists()
                or User.objects.filter(username=username).exists()
        ):
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(subject=EMAIL_SUBJECT,
                      message=f'{EMAIL_MESSAGE}: {confirmation_code}',
                      from_email=ADMIN_EMAIL,
                      recipient_list=(email,))
            response = {
                'email': email,
                'username': username
            }
            return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        current_user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(
            user=current_user,
            token=confirmation_code
        ):
            token = RefreshToken.for_user(user=current_user)
            response = {
                'token': str(token.access_token)
            }
            return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
