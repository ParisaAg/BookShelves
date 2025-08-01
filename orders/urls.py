# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CheckoutView, PaymentVerificationView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # این خط در پروژه شما وجود ندارد و باید اضافه شود
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    path('orders/verify/', PaymentVerificationView.as_view(), name='payment-verify'),
    
    path('', include(router.urls)),
]