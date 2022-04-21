
from urllib import response
from rest_framework.test import APITestCase
from rest_framework import status
from .defs.defs import *
from .test_tickers import *
import json

from transactions.models.transactions import TxHistory
from transactions.serializers import TxHistorySerializer

from coinswap.models import CustomUser
from coinswap.serializers import UserSerializer

class transactionsSaveTest(APITestCase):
    
    def test_create_transaction_airdrop_funds(self):
        #primero tiene que existir la airdrop wallet
        register_airdrop_user(self)
        #creo el ticker, el usuario admin se regitra en ese test
        tickersTest.test_createticker(self)
        response = self.adm_cliente.post('/trx/fundairdrop',{'amount':'1000','cointicker':'BTC'})
        # print(response.json())
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_request_airdrop(self):
        self.test_create_transaction_airdrop_funds()
        user_test = register_user1(self)
        response = user_test.post('/trx/requestairdrop',{'cointicker':'BTC'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_request_burn(self):
        self.test_create_transaction_airdrop_funds()
        register_burn_user(self)
        user_test = register_user1(self)
        response = user_test.post('/trx/requestairdrop',{'cointicker':'BTC'})
        response = user_test.post('/trx/requestburn',{'cointicker':'BTC','amount':'0.05'})
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    #user_test1 = 0xd65339361a81a1fdb406e456645655456e2658de
    #user_test2 = 0xd65339356456456456446e456645655456e2658e
    def test_p2p_trx(self):
        self.test_create_transaction_airdrop_funds()
        user_test1 = register_user1(self)
        user_test2 = register_user2(self)
        response1 = user_test1.post('/trx/requestairdrop',{'cointicker':'BTC'})
        self.assertEqual(response1.status_code,status.HTTP_200_OK)
        response2 = user_test2.post('/trx/requestairdrop',{'cointicker':'BTC'})
        self.assertEqual(response2.status_code,status.HTTP_200_OK)
        response1= user_test1.post('/trx/p2p',
        {'cointicker':'BTC','amount':'0.07','wallet':'0xd65339356456456456446e456645655456e2658e'})
        self.assertEqual(response1.status_code,status.HTTP_201_CREATED)

    def test_balance_show(self):
        self.test_create_transaction_airdrop_funds()
        user_test = register_user1(self)
        response = user_test.post('/trx/requestairdrop',{'cointicker':'BTC'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = user_test.get('/trx/balances/list')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(response.data)