from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAdminUser , AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.cointicker import CoinTicker
from .serializers import CoinTickerSerializer




class CoinList(APIView):
    permission_classes = [IsAuthenticated]#cualquier usuario puede ver las monedas
    def get(self, request, format=None):
        coins = CoinTicker.objects.all()
        serializer = CoinTickerSerializer(coins, many=True)
        return Response(serializer.data)
        
class CoinCreate(APIView):
    permission_classes = [IsAdminUser] #admin el único que puede crear
    def post(self, request):
        serializer = CoinTickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)