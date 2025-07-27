from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        
        extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5,
                    'error_messages': {
                    'min_value': 'امتیاز باید حداقل ۱ ستاره باشد.', 
                    'max_value': 'امتیاز باید حداکثر ۵ ستاره باشد.'
                }
                       }
        }
    def validate(self, data):

            user = self.context['request'].user
            book = self.context['book']
            comment_text = data.get('comment', '')

            if Review.objects.filter(user=user, book=book, comment__iexact=comment_text).exists():
                raise serializers.ValidationError("این نظر شما قبلا ثبت شده است. لطفا نظر تکراری قرار ندهید.")

            return data