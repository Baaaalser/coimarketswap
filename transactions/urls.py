from django.urls import path
from .views import *



urlpatterns = [
                #listados
                path('coins/list',CoinList.as_view(),name='coins_list'),
                path('balances/list',BalancesList.as_view(),name='balances_list'), 
                path('list',TxHistoryList.as_view(),name='tx_list'),
                
                path('coins/createcoins',CoinCreate.as_view(),name='coins_createcoins'),
                
                #Fondeo del wallet airdrop
                path('fundairdrop',FundAirdropWallet.as_view(),name='tx_fundairdrop'),
                path('requestairdrop',TxRequestAirdrop.as_view(),name='tx_requestairdrop'),
                #burn
                path('requestburn',TxRequestBurn.as_view(),name='tx_requestburn'),
                #P2P
                path('p2p',P2PTrx.as_view(),name='tx_p2p'),
            ]