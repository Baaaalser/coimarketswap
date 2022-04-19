from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAdminUser , AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.cointicker import CoinTicker
from .models.transactions import TxHistory
from .models.balance import Balance
from .serializers import CoinTickerSerializer,TxHistorySerializer
from coinswap.models import CustomUser
from coinswap.serializers import UserSerializer
from cryptography.fernet import Fernet
import base64
from datetime import datetime

def generateTxHash(data):# paso el dict
    if not (type(data) is dict):
        return 1
    hash_salt = Fernet(b'EWDZM_yfFkL-uJK4Qle_SJ4RYGvfxRGxYVteaEkmDdg=')# salt
    date = datetime.now() #tengo que generar antes la fecha para poder hacer hash a todo
    data['date_time'] = date
    
    
    mergedkeys = ''
    for keys in data:
        mergedkeys = ''.join(str(data[keys]))

    token = hash_salt.encrypt(bytes(mergedkeys,'utf-8'))
    hashed_data = base64.urlsafe_b64encode(token).decode("utf-8") 
    return hashed_data

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


class TxHistoryList(APIView):
	permission_classes = [IsAdminUser] #solo el admin puede ver todas
	def get(self, request):
		txhistory = TxHistory.objects.all()
		serializer = TxHistorySerializer(txhistory, many=True)
		return Response(serializer.data)


class TxHistoryCreate(APIView):
    permission_classes = [IsAdminUser] #admin el único que puede crear
    def post(self, request):
        print(request.data)
        print(request.user)
        wallet = CustomUser.objects.filter(email=request.user) #ver selectrelated para traer la wallet
        ticker_s = CoinTicker.objects.filter(ticker_symbol=request.data['cointicker'])
        # userserialize = UserSerializer(wallet)
        # print(userserialize)
        print(ticker_s[0].ticker_name)
        print(wallet[0].wallet_address)
        print(request.method)
        # print(list(request.query_params.values())[0].upper())
        print(request.query_params)
        print(request.query_params['type'].upper())
        print(request.query_params['mode'].upper())
    
        serializer = CoinTickerSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)# por ahora no guardo nada
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FundAirdropWallet(APIView):
    

    permission_classes = [IsAdminUser] #solo el admin fondear al airdrop
    def post(self,request):
        #solo el admin puede fondear (admin@coinmarketswap.com), la operación se registra como (1,'AIRDROP','DEPOSIT')
        
        userposting = request.user
        ticker = request.POST['cointicker']
        amount = float(request.POST['amount'])
        print(userposting.email)
        if(userposting.email == 'admin@coinmarketswap.com'):
            print('Entro el admin')#primero busco la wallet del airdrop
            wallet_funder = CustomUser.objects.filter(email=userposting) # para armar la transacción, el origen va a ser la root wallet
            wallet_airdrop = CustomUser.objects.filter(email='airdrop@coinmarketswap.com') # destino airdrop
            print(f'Origen : {wallet_funder[0].wallet_address}')
            if(CoinTicker.objects.filter(ticker_symbol=ticker).exists()): #existe el ticker?
                ticker_id = CoinTicker.objects.filter(ticker_symbol=ticker)[0].id
                print(ticker_id)
                #ya tengo la wallet origen/destino/monto/moneda/tipo de operacion
                previous_amount = float(0)
                if(Balance.objects.filter(wallet=wallet_airdrop[0].id).exists()):#ya tiene balance?
                    if(Balance.objects.filter(coin_ticker=ticker_id).exists):
                        previous_amount = Balance.objects.filter(coin_ticker=ticker_id,wallet=wallet_airdrop)[0].amount
                after_amount = amount + previous_amount # es un depósito, se suman
                dict_data  = {
				'tx_type' : 1 ,
				'wallet_from': wallet_funder,
				'wallet_to': wallet_airdrop,
				'ticker': ticker,
				'previous_amount': previous_amount,
				'current_amount': amount,
				'after_amount': after_amount
				}
                print(generateTxHash(dict_data))

            else:
                return Response("Ticker doesn't exists",status=status.HTTP_404_NOT_FOUND)
            
            try:
                print(f'Destino : {wallet_airdrop[0].wallet_address}')
            except IndexError:
                print('no hay datos para la búsqueda')

        else:
            return Response(status=status.HTTP_403_FORBIDDEN) #you shall not pass!!!!!
        return Response(status=status.HTTP_200_OK)

#solicito un airdrop
#para mi wallet address
#no debe tener balance previo
#necesito el ticker (dentro del request)
#la operación será del tipo : ('AIRDROP','SENT') y la tiene que enviar la wallet del "airdrop"

class TxRequestAirdrop(APIView): #para fondear la cuenta lo primero es pedir un airdrop por única vez
    permission_classes = [IsAuthenticated]#sólo lo pueden pedir usuarios registrados
    def get(self,request): 
        pass
        return Response(status=status.HTTP_200_OK)