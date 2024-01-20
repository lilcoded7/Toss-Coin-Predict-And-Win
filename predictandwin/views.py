from django.shortcuts import render, get_object_or_404
from predictandwin.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from predictandwin.models.coin import Coin
from predictandwin.models.result import Result
from predictandwin.models.user_stake import Stake
from decimal import Decimal
import random

# Create your views here.



class TossAPIView(generics.GenericAPIView):
    serializer_class = StakeSerializer
    permission_classes = [IsAuthenticated]

    def get_predict_value(self, predict_id):
        customer_predict = get_object_or_404(Coin, id=predict_id)
        return customer_predict 

    def coin_toss(self, stake):

        tossing_coin = random.choice(["HEAD", "TAIL"])
        is_winner = stake.prediction.side == tossing_coin
        result = Result.objects.create(user_stake=stake, toss_choice=tossing_coin, is_winner=is_winner)

        if not is_winner:
            return False
        return result

    def post(self, request):
        customer = request.user

        if customer.user_exist:
            return Response({'message':'Game colsed'})

        customer_prediction = request.data.get('prediction')
        predicted_coin = self.get_predict_value(customer_prediction)
        stake = Stake.objects.create(user=customer, amount=Decimal(request.data.get('amount')), prediction=predicted_coin)
        
        if not self.coin_toss(stake):
            return Response({'message':'Game Lost'})
        
        staked_amount = Decimal(request.data.get('amount')) * 2
        customer.balance += staked_amount or Decimal('0')
        customer.save()
        
        return Response({'message': 'Game win'}, 200)


class TossCoinAnalyticsAPIView(APIView):

    def get_customer_stake(self, customer):
        return Stake.objects.filter(user=customer)

    def get_customer_stake_result(self, stake):
        return Result.objects.filter(user_stake=stake).first()

    def get(self, request):
        customer = request.user 

        resbody = [
            {
                'customer_stake': StakeSerializer(self.get_customer_stake(customer), many=True).data,
                'stake_result': ResultSerializer(self.get_customer_stake_result(stake)).data
            }
            for stake in self.get_customer_stake(customer)
        ]
        return Response({'customer': resbody})



