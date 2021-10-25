from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, Review
from .validators import UNIQUE_REVIEW_VALIDATION_MESSAGE, score_validation


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    pub_date = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%dT%H:%M:%SZ')
    text = serializers.CharField()
    score = serializers.IntegerField(validators=(score_validation,))

    class Meta:
        model = Review
        exclude = ('title', )
        read_only_fields = ('title', )

    def create(self, validated_data):
        title = validated_data.get('title')
        user = self.context.get('request').user
        if len(Review.objects.filter(author=user, title=title)) != 0:
            raise ValidationError(detail=UNIQUE_REVIEW_VALIDATION_MESSAGE)
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    text = serializers.CharField()
    pub_date = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Comment
        exclude = ('review', )
        read_only_fields = ('post', )
