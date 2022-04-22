from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAdminUser , AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import CustomUser
import random
from django.dispatch import receiver

def default_wallet():
    return '0x'+'%040x' % random.getrandbits(160)# genero la wallet de usuario en la creación

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Recuperamos las credenciales y autenticamos al usuario
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)

        # Si es correcto añadimos a la request la información de sesión
        if user:
            login(request, user)
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK)

        # Si no es correcot devolvemos un error en la petición
        return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        # Borramos de la request la información de sesión
        logout(request)

        # Devolvemos la respuesta al cliente
        return Response(status=status.HTTP_200_OK)


class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        print(self.request.POST['username'])
        print(self.request.POST['password'])
        print(self.request.POST['email'])
        serializer.save(username=self.request.POST['username'],
                        password=make_password(self.request.POST['password']),
                        email = self.request.POST['email'],
                        wallet_address=default_wallet())


class UsersList(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        users = CustomUser.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


