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
