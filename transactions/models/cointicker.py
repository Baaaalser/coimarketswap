from django.db import models
# Create your models here.

class CoinTicker(models.Model):
    ticker_symbol = models.CharField(max_length=5,unique=True)
    ticker_name = models.CharField(max_length=10,unique=True)
    
    REQUIRED_FIELDS = ['ticker_symbol', 'ticker_name']

    def __str__(self):
        return self.ticker_symbol
