from django.contrib import admin
from predictandwin.models.coin import Coin
from predictandwin.models.result import Result
from predictandwin.models.user_stake import Stake

# Register your models here.


admin.site.register(Coin)
admin.site.register(Result)
admin.site.register(Stake)