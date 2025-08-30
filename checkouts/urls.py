from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckoutView, VerifyPaymentView

router = DefaultRouter()



urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/verify/", VerifyPaymentView.as_view(), name="verify-payment"),
    path('', include(router.urls)),
]
