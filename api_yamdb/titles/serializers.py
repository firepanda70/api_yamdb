import datetime as dt
from typing import List

from rest_framework import serializers

from reviews.models import Review
from .models import Catergory, Genre, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Catergory


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        if type(self.instance) is List:
            reviews = Review.objects.filter(title=self.instance[0])
        else: reviews = Review.objects.filter(title=self.instance)
        if reviews == 0:
            return 0
        return sum([review.score for review in reviews])


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Catergory.objects.all(), slug_field='slug')

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Произведение еще не вышло!')
        return value
