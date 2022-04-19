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

txtype = ((1,'AIRDROP-DEPOSIT'),(2,'AIRDROP-SENT'),(3,'BURN-SENT'),
                (4,'BURN-DEPOSIT'),(5,'P2P-SENT'),(6,'P2P-DEPOSIT'))

class TxHistorySerializer(serializers.ModelSerializer):
	

	# wallet_from = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='wallet_address'
    #  )
	# wallet_to = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='wallet_address'
    #  )
	
	# ticker = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='ticker_name'
    #  )
	

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