from coinswap.models import CustomUser
from rest_framework.test import APIClient


#usuario admin
def register_admin(self):
    self.user = CustomUser.objects.create_superuser(
                username='root',
                email='admin@coinmarketswap.com',
                password='supertest_strong_pass',
                wallet_address='0xd65339361a81a1fdb406e7999db4d386fe2658de')
    self.admin = APIClient()
    self.admin.force_login(user=self.user)
    return self.admin

# #usuarios de prueba
def register_user1(self):
    self.user1 = CustomUser.objects.create_user(
                username='test1',
                email='test1@coinswap.com',
                password='test1_strong_pass',
                wallet_address='0xd65339361a81a1fdb406e456645655456e2658de')
    self.user_test1 = APIClient()
    self.user_test1.force_login(user=self.user1)
    return self.user_test1

def register_user2(self):
    self.user2 = CustomUser.objects.create_user(
                username='test2',
                email='test2@coinswap.com',
                password='test2_strong_pass',
                wallet_address='0xd65339356456456456446e456645655456e2658e')
    self.user_test2 = APIClient()
    self.user_test2.force_login(user=self.user2)
    return self.user_test2

def register_airdrop_user(self):
    self.air_usr = CustomUser.objects.create_user(
                username='airdrop',
                email='airdrop@coinmarketswap.com',
                password='airdrop_strong_pass',
                wallet_address='0xd65339357979878978976e456645655456e2658d')
    self.airdrop = APIClient()
    self.airdrop.force_login(user=self.air_usr)
    return self.airdrop

def register_burn_user(self):
    self.burn_usr = CustomUser.objects.create_user(
                username='burn',
                email='burn@coinmarketswap.com',
                password='burn_strong_pass',
                wallet_address='0xd653393579798789712312321231655456e2658e')
    self.burn = APIClient()
    self.burn.force_login(user=self.burn_usr)
    return self.burn

#data para los tickers

data_ticker = {
    "ticker_symbol":"BTC",
    "ticker_name": "BITCOIN"
    
}
data_format_ticker={
    "ticker_symbol": {"type": "string", "required": True},
    "ticker_name": {"type": "string", "unique": True},
}

