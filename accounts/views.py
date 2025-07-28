from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import RegisterSerializer,ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import generics, viewsets
from .models import Profile

# Create your views here.
class RegisterView(APIView):

    throttle_scope = 'register'
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "your account has been successfully"}, status=status.HTTP_201_CREATED)
            return Response({
                "errors": serializer.errors,
                "message": "There was a problem with your registration data."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e),
                "message": "An unexpected error occurred during registration."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




class LoginView(APIView):

    throttle_scope = 'login'
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate using email and password
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            response = Response()
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            response.data = {
                "message": 'you are logged in now',
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
                "id": user.id,
            }
            return response
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        


class CheckAuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "authenticated": True,
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })




class LogoutView(APIView):
    def post(self, request):
        response = Response({"message":'you are logged out now'}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return 
        


class ProfileView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
