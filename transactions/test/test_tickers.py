from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .defs.defs import *

from django.test import TestCase

from transactions.models.cointicker import CoinTicker
from transactions.serializers import CoinTickerSerializer

class TickersTest(APITestCase):
    
    def init(self):
        definitions.setUp(self)
    
    def test_createticker(self):
        # # solo admin
        self.init()
        response = self.client.post("/trx/coins/createcoins", format="json", data=definitions.data_ticker)
        is_valid = CoinTickerSerializer.validate(response.data,definitions.data_format_ticker)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(is_valid)
        self.assertEqual(response.data["ticker_symbol"], CoinTicker.objects.first().ticker_symbol)

    def test_createticker_bad(self):
        # # solo admin
        self.init()
        response = self.client.post("/trx/coins/createcoins", format="json", data={"ticker_symbol":"BTC"})
        is_valid = CoinTickerSerializer.validate(response.data,definitions.data_format_ticker)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)