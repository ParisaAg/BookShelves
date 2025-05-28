from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User  

# Create your views here.
class RegisterView(APIView):
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
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)

        if user is not None:
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
        


