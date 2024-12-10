import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# User Registration View
class UserRegisterView(APIView):
    permission_classes = [AllowAny]  # This will allow unauthenticated users to access this view

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # Generate JWT Token
            payload = {
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration (1 day)
                'iat': datetime.utcnow(),  # Issued at
            }
            
            # Secret key for signing the JWT (it can be any string)
            secret_key = settings.SECRET_KEY  # Or any other secret key you want to use
            
            # Generate the token using the HS256 algorithm
            token = jwt.encode(payload, secret_key, algorithm='HS256')

            # Return the token as part of the response
            return Response({"token": token, "access": access_token}, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
