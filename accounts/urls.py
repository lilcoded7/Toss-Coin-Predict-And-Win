from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
]