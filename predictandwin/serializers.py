from rest_framework import serializers
from predictandwin.models.user_stake import Stake
from predictandwin.models.result import Result
from predictandwin.models.coin import Coin


class StakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stake
        fields = ['prediction', 'amount']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
