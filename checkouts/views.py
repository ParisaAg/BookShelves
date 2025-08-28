import requests
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cart.models import Cart
from orders.models import Order, OrderItem
from .models import Payment

ZARINPAL_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_STARTPAY_URL = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
MERCHANT_ID = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = getattr(user, "cart", None)
        if not cart or not cart.items.exists():
            return Response({"error": "سبد خرید خالی است."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # ایجاد سفارش
            order = Order.objects.create(user=user, address=request.data.get("address", ""))
            total_price = 0
            for item in cart.items.all():
                OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
                total_price += item.total_price
            cart.clear()

            # ایجاد رکورد پرداخت
            payment = Payment.objects.create(
                order=order,
                user=user,
                method="online",
                amount=total_price,
                status="initiated"
            )

            # درخواست زرین‌پال
            data = {
                "merchant_id": MERCHANT_ID,
                "amount": total_price,
                "description": f"سفارش #{order.id}",
                "callback_url": "http://localhost:8000/api/checkout/verify/",
                "metadata": {"email": user.email},
            }
            response = requests.post(ZARINPAL_REQUEST_URL, json=data).json()

            if response.get("data") and response["data"]["code"] == 100:
                authority = response["data"]["authority"]
                payment.authority = authority
                payment.status = "pending"
                payment.save()
                return Response({"url": ZARINPAL_STARTPAY_URL.format(authority=authority)})
            else:
                return Response({"error": "خطا در اتصال به زرین‌پال"}, status=500)


class VerifyPaymentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        authority = request.GET.get("Authority")
        status_param = request.GET.get("Status")

        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:
            return Response({"error": "پرداخت یافت نشد."}, status=404)

        if status_param != "OK":
            payment.status = "canceled"
            payment.save()
            return Response({"status": "پرداخت لغو شد."})

        data = {
            "merchant_id": MERCHANT_ID,
            "amount": payment.amount,
            "authority": authority,
        }
        response = requests.post(ZARINPAL_VERIFY_URL, json=data).json()

        if response.get("data") and response["data"]["code"] == 100:
            payment.status = "successful"
            payment.ref_id = response["data"]["ref_id"]
            payment.save()
            payment.order.status = "paid"
            payment.order.save()
            return Response({"status": "پرداخت موفق", "ref_id": payment.ref_id})
        else:
            payment.status = "failed"
            payment.save()
            return Response({"status": "پرداخت ناموفق"}, status=400)
