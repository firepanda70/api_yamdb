from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import get_confirmation_code, get_token, UserViewSet

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(prefix="users", viewset=UserViewSet, basename="user")

urlpatterns = [
    path('v1/auth/signup/', get_confirmation_code, name='get_confirmation_code'),
    path('v1/auth/token', get_token, name='send_token'),
    path('v1/', include(router_v1.urls)),
]
