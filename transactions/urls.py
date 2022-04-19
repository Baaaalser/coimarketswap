from django.urls import path
from .views import CoinList,CoinCreate,TxHistoryList,TxHistoryCreate,FundAirdropWallet



urlpatterns = [
                path('coins/showcoins',CoinList.as_view(),name='coins_showcoins'),
                path('coins/createcoins',CoinCreate.as_view(),name='coins_createcoins'),
                path('tx/list',TxHistoryList.as_view(),name='tx_list'),
                path('tx/sent',TxHistoryCreate.as_view(),name='tx_sent'),
                #Fondeo del wallet airdrop
                path('tx/fundairdrop',FundAirdropWallet.as_view(),name='tx_fundairdrop'),
            ]