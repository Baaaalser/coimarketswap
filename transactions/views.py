from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAdminUser , AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.cointicker import CoinTicker
from .models.transactions import TxHistory
from .models.balance import Balance
from .serializers import *
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
    else: # si no tiene balance lo creo
        dict_data  = {
                'wallet' : wallet,
                'coin_ticker' : ticker,
                'amount': amount,
                }

        serializer = BalanceSerializer(data=dict_data)
        if serializer.is_valid():
                serializer.save()
                print('balance actualizado')
                return 0
        else:
            return 1


def saveTransaction(tx_type : str, wallet_origin:int,wallet_destination:int,
                    ticker:int, current_amount: float):

    previous_amount_origin = float(0)
    previous_amount_destination = float(0)
    current_amount = float(current_amount)
    after_amount_from = float(0)
    after_amount_to =  float(0)
    date = datetime.now() #tengo que generar antes la fecha para poder hacer hash a todo
    #guardo el emisor, en el caso de carga de fondos del airdrop al root que esta en modo dios no lo cargo en balances del emisor
    if not (wallet_destination == CustomUser.objects.filter(email='airdrop@coinmarketswap.com')[0].id):
        if(Balance.objects.filter(wallet=wallet_origin,coin_ticker=ticker).exists()):#ya tiene balance de este ticker?
            previous_amount_origin = Balance.objects.filter(wallet=wallet_origin,coin_ticker=ticker)[0].amount
            if( previous_amount_origin >= current_amount): # tienen fondos para enviar?
                if(saveBalance(wallet_origin,ticker,(previous_amount_origin-current_amount))==1): # el que envia resta
                    return 1
                after_amount_from = previous_amount_origin-current_amount
            else:
                return 1
        else:
            return 1 # si no tiene el ticker o balances de ningún tipo...
    else: #si es para fondear el airdrop tengo que pedir los fondos antes
        if(Balance.objects.filter(wallet=wallet_destination,coin_ticker=ticker).exists()):
            previous_amount_destination = Balance.objects.filter(wallet=wallet_destination,coin_ticker=ticker)[0].amount
    #guardo el receptor
    if(saveBalance(wallet_destination,ticker,(previous_amount_destination+current_amount))==1):
        return 1 
    after_amount_to = previous_amount_destination+current_amount
    dict_data  = {
                    'tx_type' : tx_type,
                    'wallet_from': wallet_origin,
                    'wallet_to': wallet_destination,
                    'ticker': ticker,
                    'previous_amount_from': previous_amount_origin,
                    'current_amount': current_amount,
                    'after_amount_from': after_amount_from,
                    'previous_amount_to': previous_amount_destination,
                    'after_amount_to' : after_amount_to,
                    'date_time' : date
                    }
    tx_hash = generateTxHash(dict_data) #obtengo el hash
    print(tx_hash)
    dict_data['tx_hash']=tx_hash
    serializer = TxHistorySerializer(data=dict_data) #salvo la transacción
    if serializer.is_valid():
        serializer.save()
        return 0

    return 1



class CoinList(APIView):
    permission_classes = [IsAuthenticated]#cualquier usuario puede ver las monedas
    def get(self, request):
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
	# permission_classes = [IsAdminUser] #solo el admin puede ver todas
    def get(self, request):
        if request.user.is_staff:
            txhistory = TxHistory.objects.all()
            serializer = TxHistoryShowSerializer(txhistory, many=True)
            return Response(serializer.data)

        elif request.user.is_authenticated:
            txhistory = TxHistory.objects.filter(wallet_from=request.user)|TxHistory.objects.filter(wallet_to=request.user)
            serializer = TxHistoryShowSerializer(txhistory, many=True)
            return Response(serializer.data)

class BalancesList(APIView):
    
    #permission_classes = [IsAdminUser] #solo el admin puede ver todos los balances
    
    def get(self, request):
        
        if request.user.is_staff:
            balances = Balance.objects.all()
            serializer = BalanceSerializer(balances, many=True)
            return Response(serializer.data)

        elif request.user.is_authenticated:
            balances = Balance.objects.filter(wallet=request.user)
            serializer = userBalanceSerializer(balances, many=True)
            return Response(serializer.data)



class FundAirdropWallet(APIView):
    permission_classes = [IsAdminUser] #solo el admin fondear al airdrop
    def post(self,request):
        #solo el admin puede fondear (admin@coinmarketswap.com), la operación se registra como (1,'AIRDROP','DEPOSIT')
        try:
            userposting = request.user
            ticker = request.POST['cointicker']
            amount = float(request.POST['amount'])
        except MultiValueDictKeyError:
            print('Error')
            return Response('missing data, use http://url/trx/tx/fundairdrop?&amount=value&cointicker=cointicker',
            status=status.HTTP_400_BAD_REQUEST)

        print(userposting.email)
        if(userposting.email == 'admin@coinmarketswap.com'):
            #primero busco la wallet del airdrop
            wallet_funder = CustomUser.objects.filter(email=userposting) # para armar la transacción, el origen va a ser la root wallet
            wallet_airdrop = CustomUser.objects.filter(email='airdrop@coinmarketswap.com') # destino airdrop
            # print(f'Origen : {wallet_funder[0].wallet_address}')
            if(CoinTicker.objects.filter(ticker_symbol=ticker).exists()): #existe el ticker?
                ticker_id = CoinTicker.objects.filter(ticker_symbol=ticker)[0].id
                #ya tengo la wallet origen/destino/monto/moneda/tipo de operacion/fecha y el hash de la transacción
                if(saveTransaction('airdrop',wallet_funder[0].id,wallet_airdrop[0].id,ticker_id,amount)==1):
                    return Response("Couldn't complete the request",status=status.HTTP_403_FORBIDDEN)
            else:
                return Response("Ticker doesn't exists",status=status.HTTP_404_NOT_FOUND)
            try:
                print(f'Destino : {wallet_airdrop[0].wallet_address}')
            except IndexError:
                print('no hay datos para la búsqueda')

        else:
            return Response(status=status.HTTP_403_FORBIDDEN) #you shall not pass!!!!!
        return Response(status=status.HTTP_200_OK)



class TxRequestAirdrop(APIView): #para fondear la cuenta lo primero es pedir un airdrop por única vez
    permission_classes = [IsAuthenticated]#sólo lo pueden pedir usuarios registrados
    def post(self,request): 
        try:
            userposting = request.user
            ticker = request.POST['cointicker']
        except MultiValueDictKeyError:
            print('Error')
            return Response('missing data, use http://url//trx/tx/requestairdrop?&cointicker=ticker',
            status=status.HTTP_400_BAD_REQUEST)
        amount = float(10)# dejo fijo en 10 el monto del airdrop
        wallet_airdrop = CustomUser.objects.filter(email='airdrop@coinmarketswap.com') # origen airdrop
        if not (userposting.email == 'admin@coinmarketswap.com'): #no tiene sentido que el admin pida fondos
            wallet_destination = CustomUser.objects.filter(email=userposting)
            # verificar si la cuenta solicitante tiene el ticker, asi limito a un airdrop por ticker
            if(CoinTicker.objects.filter(ticker_symbol=ticker).exists()): #existe el ticker?
                ticker_id = CoinTicker.objects.filter(ticker_symbol=ticker)[0].id
                if (Balance.objects.filter(coin_ticker=ticker_id,wallet=wallet_destination[0].id)): #Si la wallet ya tiene balance para ese ticker, rechazo el pedido
                    return Response(f"You can request airdrop for {ticker} only once",status=status.HTTP_403_FORBIDDEN) #you shall not pass!!!!!
                else:# le mando el airdrop (2,'AIRDROP-SENT')
                    saveTransaction('airdrop',wallet_airdrop[0].id,wallet_destination[0].id,ticker_id,amount)
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response("Ticker doesn't exists",status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Admin users can't request funds...",status=status.HTTP_403_FORBIDDEN) #you shall not pass!!!!!
        

class TxRequestBurn(APIView):
    permission_classes = [IsAuthenticated]#sólo lo pueden pedir usuarios registrados
    def post(self,request): 
        userposting = request.user
        ticker = request.POST['cointicker']
        amount = request.POST['amount']
        wallet_burn = CustomUser.objects.filter(email='burn@coinmarketswap.com') # destino burn wallet (3,'BURN-SENT')
        wallet_origin = CustomUser.objects.filter(email=userposting) # origen 
        if(CoinTicker.objects.filter(ticker_symbol=ticker).exists()): #existe el ticker?
                ticker_id = CoinTicker.objects.filter(ticker_symbol=ticker)[0].id
                if(saveTransaction('burn',wallet_origin[0].id,wallet_burn[0].id,ticker_id,amount)==0):
                    return Response('ok',status=status.HTTP_200_OK)
                else:
                    return Response("Couldn't complete the request",status=status.HTTP_403_FORBIDDEN)
        else:
                return Response("Ticker doesn't exists",status=status.HTTP_404_NOT_FOUND)


class P2PTrx(APIView):
    permission_classes = [IsAuthenticated] #solo el admin fondear al airdrop
    def post(self,request):
        #solo el admin puede fondear (admin@coinmarketswap.com), la operación se registra como (5,'P2P-SENT')
        userposting = request.user
        ticker = request.POST['cointicker']
        amount = float(request.POST['amount'])
        wallet_destination = CustomUser.objects.filter(wallet_address=request.POST['wallet']) # destino 
        #primero busco la wallet
        wallet_origin = CustomUser.objects.filter(email=userposting) #wallet origen
        
        
        if(CoinTicker.objects.filter(ticker_symbol=ticker).exists()): #existe el ticker?
            ticker_id = CoinTicker.objects.filter(ticker_symbol=ticker)[0].id
            
            if(saveTransaction('p2p',wallet_origin[0].id,wallet_destination[0].id,ticker_id,amount)==1):
                return Response("Couldn't complete the request",status=status.HTTP_403_FORBIDDEN)

        else:
            return Response("Ticker doesn't exists",status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)