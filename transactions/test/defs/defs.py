from coinswap.models import CustomUser
class definitions():

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(
            username='supertest',
            email='supertest@bar.com',
            password='supertest_strong_pass')
        self.client.force_login(user=self.user)
        return self.client
    data_ticker = {
        "ticker_symbol":"BTC",
        "ticker_name": "BITCOIN"
        
    }
    data_format_ticker={
        "ticker_symbol": {"type": "string", "required": True},
        "ticker_name": {"type": "string", "unique": True},
    }