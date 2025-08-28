from django.urls import path
from .views import CheckoutView, VerifyPaymentView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/verify/", VerifyPaymentView.as_view(), name="verify-payment"),
]
