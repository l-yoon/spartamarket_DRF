from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .validators import validate_signup
from .serializers import UserSerializer

User = get_user_model()
#회원가입
class SignupView(APIView):
    
    def post(self, request):
        is_valid, error_msg =validate_signup(request.data)
        if not is_valid:
            return Response({"error": error_msg}, status=400)
        
        user = User.objects.create_user(**request.data)
        
        serializer = UserSerializer(user)
        return Response(serializer.data) 
    
#로그인
class LoginView(APIView):
    def post(self, request):
        user = authenticate(**request.data)
        
        if not user:
            return Response({"error": "아이디 또는 비밀번호가 올바르지 않습니다"}, status=400)
        res_data = UserSerializer(user).data
        
        #token
        refresh = RefreshToken.for_user(user)
        res_data['access_token'] = str(refresh.access_token)
        res_data['refresh_token'] = str(refresh)
        return Response(res_data) 

#로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data["refresh_token"]
        
        try:
            token = RefreshToken(refresh_token)
        except TokenError:
            return Response( {"error": "token이 없습니다"}, status=400)
        
        token.blacklist()
        return Response(status=200)

#프로필 조회
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)