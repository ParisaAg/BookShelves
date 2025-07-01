from rest_framework import serializers
from .models import Review
from django.db.models import Avg
from books.models import Book





class BookDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('rating'))['avg']

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'average_rating',]



class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Review
        fields = ['id', 'book', 'rating', 'comment']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']

        review, created = Review.objects.update_or_create(
            user=user,
            book=book,
            defaults={
                'rating': validated_data['rating'],
                'comment': validated_data.get('comment', '')
            }
        )
        return review
