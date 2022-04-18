from rest_framework import serializers
from .models.cointicker import CoinTicker

class CoinTickerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoinTicker
		fields ='__all__'