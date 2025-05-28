from .views import OrderCreateView,UserOrderListView,OrderDetailView,CancelOrderView,OrderInvoiceView
from django.urls import path

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('my-orders/', UserOrderListView.as_view(), name='user-orders'),
    path('my-orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('my-orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('<int:pk>/invoice/', OrderInvoiceView.as_view(), name='order-invoice'),

]