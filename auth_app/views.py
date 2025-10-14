from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            user = s.save()
            logger.info(f"new user register {user.username}")
            return Response({"message": "user registered"}, status=201)
        logger.warning(f"registration failed: {s.errors}")
        return Response(s.errors, status=400)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request):
        logger.info(f"profile viewed {request.user.username}")
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        s = UserSerializer(request.user, data=request.data, partial=True)
        
        if s.is_valid():
            s.save()
            logger.info(f"profile updated {request.user.username}")
            return Response(s.data)
        
        logger.warning(f"profile update failed for {request.user.username}: {s.errors}")
        return Response(s.errors, status=400)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            logger.info(f"user {request.user.username} logged out")
            return Response(status=205)
        except Exception as e:
            logger.error(f"logout failed for {request.user.username}: {e}")
            return Response({"detail": "invalid token"}, status=400)
