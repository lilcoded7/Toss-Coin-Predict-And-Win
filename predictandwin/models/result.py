from django.db import models
from setup.basemodel import TimeBaseModel
from predictandwin.models.user_stake import Stake

class Result(TimeBaseModel):
    user_stake = models.ForeignKey(Stake, on_delete=models.CASCADE)
    toss_choice = models.CharField(max_length=4)
    is_winner = models.BooleanField(default=False)


    def __str__(self):
        return f"Customer: {self.user_stake.user.get_username}  Pridicted: {self.user_stake.prediction} Amount: {self.user_stake.amount}"