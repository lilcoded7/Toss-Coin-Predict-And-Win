from django.urls import path
from predictandwin.views import *


urlpatterns = [
    path('toss/coin/', TossAPIView.as_view(), name='toss- coin'),
    path('customer/toss/analytics/', TossCoinAnalyticsAPIView.as_view())
]