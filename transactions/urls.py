from django.urls import path
from .views import CoinList,CoinCreate



urlpatterns = [
                path('coins/showcoins',CoinList.as_view(),name='coins_showcoins'),
                path('coins/createcoins',CoinCreate.as_view(),name='coins_createcoins'),
            ]