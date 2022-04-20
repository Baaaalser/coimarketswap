from django.urls import path
from .views import *



urlpatterns = [
                #listados
                path('coins/showcoins',CoinList.as_view(),name='coins_showcoins'),
                path('balances/list',BalancesList.as_view(),name='balances_list'), 
                path('tx/list',TxHistoryList.as_view(),name='tx_list'),
                
                path('coins/createcoins',CoinCreate.as_view(),name='coins_createcoins'),
                
                #Fondeo del wallet airdrop
                path('tx/fundairdrop',FundAirdropWallet.as_view(),name='tx_fundairdrop'),
                path('tx/requestairdrop',TxRequestAirdrop.as_view(),name='tx_requestairdrop'),
                #burn
                path('tx/requestburn',TxRequestBurn.as_view(),name='tx_requestburn'),
                #P2P
                path('tx/p2p',P2PTrx.as_view(),name='tx_p2p'),
            ]