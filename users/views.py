from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

import json

from users.permissions import CustomReadOnly
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer


# Create your views here.
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [CustomReadOnly]

    def get(self, request, pk=None, *args, **kwargs):
        uid = pk or kwargs.get('pk')
        user = User.objects.get(id=uid)

        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None, *args, **kwargs):
        print(request.user.id)
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(id=user.id, username=user.username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR, )


class GetMyProfile(APIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get(self, request, *args, **kwargs):
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'logout': True}, status=status.HTTP_200_OK)
