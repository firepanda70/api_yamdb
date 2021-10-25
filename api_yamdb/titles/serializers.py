from rest_framework import serializers

from .models import Catergory, Genre, Title
from .validators import year_validation


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
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def get_rating(self, obj):
        if not obj.reviews.exists():
            return None
        rewiews = obj.reviews.all()
        return sum([review.score for review in rewiews]) / len(rewiews)


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Catergory.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(validators=(year_validation,))

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
