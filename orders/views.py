from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Order

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        data = []
        for order in orders:
            data.append({
                "id": order.id,
                "status": order.status,
                "total_price": order.total_price,
                "items": [
                    {"book": item.book.title, "quantity": item.quantity, "price": item.price}
                    for item in order.items.all()
                ]
            })
        return Response(data)
