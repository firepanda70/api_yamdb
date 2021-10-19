from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from .filters import TitleFilter
from reviews.models import Title, Catergory, Genre, Review
from .permissions import AuthorModerAdminOrReadOnly
from .serializers import (
    TitleSerializer,
    TitleCreateUpdateSerializer,
    CategorySerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer
)



class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class TitleListCreateViewSet(ListCreateViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return TitleCreateUpdateSerializer
        return TitleSerializer

    def create(self, request):
        serializer = TitleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        queryset_after_creation = Title.objects.all()
        name_after_creation = serializer.data['name']
        title_after_creation = get_object_or_404(
            queryset_after_creation,
            name=name_after_creation
        )
        serializer_after_creation = TitleSerializer(title_after_creation)
        return Response(serializer_after_creation.data)


class TitleRetrieveUpdateDestroyViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        serializer = TitleSerializer(title)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        serializer = TitleCreateUpdateSerializer(title, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        queryset_after_update = Title.objects.all()
        title_after_update = get_object_or_404(queryset_after_update, pk=pk)
        serializer_after_update = TitleSerializer(title_after_update)
        return Response(serializer_after_update.data)

    def destroy(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateViewSet(ListCreateViewSet):
    queryset = Catergory.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDestroyViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        queryset = Catergory.objects.all()
        category = get_object_or_404(queryset, slug=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreListCreateViewSet(ListCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDestroyViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        queryset = Genre.objects.all()
        category = get_object_or_404(queryset, slug=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

