from random import choices
from secrets import choice
from rest_framework import serializers
from .models.cointicker import CoinTicker
from .models.transactions import TxHistory
from .models.balance import Balance

class CoinTickerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoinTicker
		fields ='__all__'



class TxHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TxHistory
		fields = '__all__'

class TxHistoryShowSerializer(serializers.ModelSerializer):
	

	wallet_from = serializers.SlugRelatedField(
        read_only=True,
        slug_field='wallet_address'
    )
	wallet_to = serializers.SlugRelatedField(
        read_only=True,
        slug_field='wallet_address'
    )
	
	ticker = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ticker_name'
    )
	

	class Meta:
		model = TxHistory
		fields = '__all__'
		

class BalanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Balance
		fields = '__all__'

class userBalanceSerializer(serializers.ModelSerializer):
	wallet = serializers.SlugRelatedField(
        read_only=True,
        slug_field='wallet_address'
    )
	coin_ticker = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ticker_name'
    )
	class Meta:
		model = Balance
		fields = '__all__'