
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')), 
    path('api/', include('books.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/carts/', include('carts.urls')),
    path('postgresql/', include('postgresql_app.urls')),
    path('api/sliders/', include('sliders.urls')),
    path('api/reviews/', include('reviews.urls')),


]
