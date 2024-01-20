from django.db import models
from setup.basemodel import TimeBaseModel

class Coin(TimeBaseModel):
    side = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f"Select Coin Side: {self.side}"