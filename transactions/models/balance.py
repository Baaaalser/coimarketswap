from django.db import models
from coinswap.models import CustomUser
from .cointicker import CoinTicker
# Create your models here.

class Balance(models.Model):
    wallet = models.ForeignKey(CustomUser, related_name='wallet_address', on_delete=models.CASCADE)
    deposit_date = models.DateTimeField(auto_now_add=True) #fecha del 1er depósito
    last_up_date = models.DateTimeField(auto_now=True) #última actualización
    coin_ticker = models.ForeignKey(CoinTicker, related_name='ticker_symbol', on_delete=models.CASCADE)#moneda
    amount = models.FloatField()

    
    def __str__(self):
        return self.ticker_symbol