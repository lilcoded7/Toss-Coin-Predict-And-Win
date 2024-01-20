from django.db import models
from setup.basemodel import TimeBaseModel
from django.contrib.auth import get_user_model
from predictandwin.models.coin import Coin

User = get_user_model()

class Stake(TimeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    prediction = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        return f"Customer: {self.user.get_username} Amount: {self.amount} Predicted: {self.prediction}"