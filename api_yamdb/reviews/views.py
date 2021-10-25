from api.permissions import AuthorModerAdminOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Review, Title
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModerAdminOrReadOnly, )

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title, id=title_id))

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModerAdminOrReadOnly, )

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review, id=review_id),)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, id=title_id)
        return get_object_or_404(Review, id=review_id).comments.all()
