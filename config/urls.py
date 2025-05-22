
from django.contrib import admin
from django.urls import path,include
from accounts.views import db_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')), 
    path("api/dbcheck/", db_check),
    path('api/', include('books.urls')),

]
