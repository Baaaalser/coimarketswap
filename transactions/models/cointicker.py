from django.db import models
# Create your models here.

class CoinTicker(models.Model):
    ticker_symbol = models.CharField(max_length=5)
    ticker_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.ticker_symbol
