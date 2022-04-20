from django.db import models
from coinswap.models import CustomUser
from .cointicker import CoinTicker

class TxHistory(models.Model):

    
    tx_hash = models.CharField(max_length=160,unique=True)
    tx_type = models.CharField(max_length=7)
    wallet_from = models.ForeignKey(CustomUser, related_name='wallet_f', on_delete=models.RESTRICT)
    wallet_to = models.ForeignKey(CustomUser, related_name='wallet_t', on_delete=models.RESTRICT)
    ticker = models.ForeignKey(CoinTicker,related_name='coin_ticker',on_delete=models.CASCADE)
    previous_amount = models.FloatField(default=0)
    current_amount = models.FloatField(default=0)
    after_amount = models.FloatField(default=0)
    date_time = models.DateTimeField()