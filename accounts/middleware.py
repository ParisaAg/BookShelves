from django.core.cache import cache
from django.utils import timezone

class OnlineUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            cache_key = f'online-user-{request.user.id}'
            cache.set(cache_key, now, 300) 
        
        response = self.get_response(request)
        return response