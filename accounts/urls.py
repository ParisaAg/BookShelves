
from django.urls import path,include
from .views import RegisterView,LoginView,UserProfileView,LogoutView,CheckAuthView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
]

