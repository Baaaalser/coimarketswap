from rest_framework.test import APITestCase
from rest_framework import status
from .defs.defs import *


from transactions.models.cointicker import CoinTicker
from transactions.serializers import CoinTickerSerializer

class tickersTest(APITestCase):
    
    def test_createticker(self):
        # # solo admin
        self.adm_cliente = register_admin(self)
        response = self.adm_cliente.post("/trx/coins/createcoins", format="json", data=data_ticker)
        is_valid = CoinTickerSerializer.validate(response.data,data_format_ticker)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(is_valid)
        self.assertEqual(response.data["ticker_symbol"], CoinTicker.objects.first().ticker_symbol)
        return self.adm_cliente

    def test_createticker_bad(self):
        # # solo admin
        adm_cliente = register_admin(self)
        response = adm_cliente.post("/trx/coins/createcoins", format="json", data={"ticker_symbol":"BTC"})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)