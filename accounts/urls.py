
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView,LoginView,ProfileView,LogoutView,CheckAuthView,AddressViewSet


router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('', include(router.urls)),

]


