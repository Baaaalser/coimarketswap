from functools import partial
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAdminUser , AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.cointicker import CoinTicker
from .models.transactions import TxHistory
from .models.balance import Balance
from .serializers import CoinTickerSerializer,TxHistorySerializer,BalanceSerializer,TxHistoryShowSerializer
from coinswap.models import CustomUser
from coinswap.serializers import UserSerializer
from cryptography.fernet import Fernet
import base64
from datetime import datetime

def generateTxHash(data):# paso el dict
    if not (type(data) is dict):
        return 1
    hash_salt = Fernet(b'EWDZM_yfFkL-uJK4Qle_SJ4RYGvfxRGxYVteaEkmDdg=')# salt
    mergedkeys = ''
    for keys in data:
        mergedkeys = ''.join(str(data[keys]))

    token = hash_salt.encrypt(bytes(mergedkeys,'utf-8'))
    hashed_data = base64.urlsafe_b64encode(token).decode("utf-8") 
    return hashed_data

# Registro de transacciones
def saveBalance(wallet:int,ticker:int,amount:float):

    

    if(Balance.objects.filter(wallet=wallet,coin_ticker=ticker).exists()): #existe balance para esa wallet?
        #actualizo en ese caso
        balance_id = Balance.objects.filter(wallet=wallet,coin_ticker=ticker)
        to_edit = Balance.objects.get(id=balance_id[0].id)
        to_edit.amount = amount
        to_edit.save()
        print('balance actualizado')
        return Response(status=status.HTTP_201_CREATED)

    dict_data  = {
            'wallet' : wallet,
            'coin_ticker' : ticker,
            'amount': amount,
            }

    serializer = BalanceSerializer(data=dict_data)
    if serializer.is_valid():
            serializer.save()
            print('balance actualizado')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    pass
    return 0

def saveTransaction(tx_type : int, wallet_origin:int,wallet_destination:int,
                    ticker:int,previous_amount: float, current_amount: float,after_amount: float,
                    date : datetime):

    
    dict_data  = {
				'tx_type' : tx_type,
				'wallet_from': wallet_origin,
				'wallet_to': wallet_destination,
				'ticker': ticker,
				'previous_amount': previous_amount,
				'current_amount': current_amount,
				'after_amount': after_amount,
                'date_time' : date
				}
    tx_hash = generateTxHash(dict_data) #obtengo el hash
    print(tx_hash)
    dict_data['tx_hash']=tx_hash
    serializer = TxHistorySerializer(data=dict_data)

    if serializer.is_valid():
        serializer.save()
        #una vez salvada la transaccion actualizo los balances
        #hago un backup de ambas wallets
        #guardo el emisor, en el caso de carga de fondos del airdrop al root que esta en modo dios no lo cargo en balances del emisor
        if not (tx_type == 1):
            saveBalance(wallet_origin,ticker,after_amount)
        #guardo el receptor
        saveBalance(wallet_destination,ticker,after_amount)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
		serializer = TxHistoryShowSerializer(txhistory, many=True)
		return Response(serializer.data)

class BalancesList(APIView):
	permission_classes = [IsAdminUser] #solo el admin puede ver todos los balances
	def get(self, request):
		balances = Balance.objects.all()
		serializer = BalanceSerializer(balances, many=True)
		return Response(serializer.data)



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
                    if(Balance.objects.filter(coin_ticker=ticker_id).exists()):
                        previous_amount = Balance.objects.filter(coin_ticker=ticker_id,wallet=wallet_airdrop[0].id)[0].amount
                after_amount = amount + previous_amount # es un depósito, se suman
                date = datetime.now() #tengo que generar antes la fecha para poder hacer hash a todo
                dict_data  = {
				'tx_type' : 1 ,
				'wallet_from': wallet_funder,
				'wallet_to': wallet_airdrop,
				'ticker': ticker,
				'previous_amount': previous_amount,
				'current_amount': amount,
				'after_amount': after_amount,
                'date_time' : date
				}
                
                #ya tengo la wallet origen/destino/monto/moneda/tipo de operacion/fecha y el hash de la transacción
                saveTransaction(1,wallet_funder[0].id,wallet_airdrop[0].id,ticker_id,previous_amount,amount,after_amount,date)
                # cargar la transaccion si sale ok actualizar el balance

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

