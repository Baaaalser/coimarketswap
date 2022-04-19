from rest_framework import serializers
from .models.cointicker import CoinTicker
from .models.transactions import TxHistory

class CoinTickerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoinTicker
		fields ='__all__'

class TxHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TxHistory
		fields = '__all__'