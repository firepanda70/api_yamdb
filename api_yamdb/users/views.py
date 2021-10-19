from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet


from .serializers import ConfirmationCodeSerializer, TokenSerializer, UserSerializer
from api.permissions import IsAdmin

EMAIL_SUBJECT = 'Подтверждение регистрации на YaMDb'
EMAIL_MESSAGE = 'Код подтверждения регистрации:'
EMAIL_SENDED_MESSAGE = 'Код подтверждения отправлен на email '
ADMIN_EMAIL = "no-replay@example.com"

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code = default_token_generator.make_token(username)

        if not User.objects.filter(email=email, username=username).exists():
            User.objects.create_user(email=email)

        send_mail(subject=EMAIL_SUBJECT,
                  message=f'EMAIL_MESSAGE {confirmation_code}',
                  from_email=ADMIN_EMAIL,
                  recipient_list=(email,))
        return Response(data=f'EMAIL_SENDED_MESSAGE {email}', status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        current_user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user=current_user, token=confirmation_code):
            token = RefreshToken.for_user(user=current_user)
            response = {
                "access_token": str(token.access_token)
            }
            return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data)
        if request.method == "PATCH":
            user = get_object_or_404(User, username=self.request.user)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )
