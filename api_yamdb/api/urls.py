from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import CommentViewSet, ReviewViewSet
from titles.views import (CategoryDestroyViewSet, CategoryListCreateViewSet,
                          GenreDestroyViewSet, GenreListCreateViewSet,
                          TitleListCreateViewSet,
                          TitleRetrieveUpdateDestroyViewSet)
from users.views import UserViewSet, get_confirmation_code, get_token

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(prefix='users', viewset=UserViewSet, basename="user")
router_v1.register('titles', TitleListCreateViewSet, basename='titles')
router_v1.register(
    'titles',
    TitleRetrieveUpdateDestroyViewSet,
    basename='title'
)
router_v1.register(
    'categories',
    CategoryListCreateViewSet,
    basename='categories'
)
router_v1.register('categories', CategoryDestroyViewSet, basename='category')
router_v1.register('genres', GenreListCreateViewSet, basename='genres')
router_v1.register('genres', GenreDestroyViewSet, basename='genre')
router_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/signup/',
         get_confirmation_code,
         name='get_confirmation_code'),
    path('v1/auth/token/', get_token, name='send_token'),
    path('v1/', include(router_v1.urls)),
]
