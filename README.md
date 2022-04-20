# coimarketswap
simulación de capa Swap sobre blockchain

Prerequisitos:

Se necesita un usuario admin que tendrá acceso a todas las funciones de la plataforma, para crearlo se realiza de la siguiente forma:
```bash
python manage.py createsuperuser 
```
Es necesario un usuario "airdrop@coinmarketswap.com" quien tendrá las carteras con el disponible para airdrops
y un usuario "burn@coinmarketswap.com" destino de la quema de monedas

la creación de usuarios para la plataforma se realiza en el siguiente endpoint:

http://192.168.1.115:8000/api/auth/signup/

se envía:
```json
{
    "email": "usertest4@mail.com",
    "username": "usertest4",
    "password": "usertest4134"
}
```
responde;
```json
{
	"id": 7,
	"email": "usertest4@mail.com",
	"username": "usertest4",
	"wallet_address": "0x2516533a54affb142f1490d3485db410ee5d8c21"
}
```
el login(se guarda un cookie de sesión):

http://192.168.1.115:8000/api/auth/login/

se envía:
```json
{
    "email": "usertest4@mail.com",
    "username": "usertest4",
    "password": "usertest4134"
}
```
responde;
```json
{
	"id": 7,
	"email": "usertest4@mail.com",
	"username": "usertest4",
	"wallet_address": "0x2516533a54affb142f1490d3485db410ee5d8c21"
}
```
el logout:

http://192.168.1.115:8000/api/auth/logout/

Para crear ticker(sólo admin):

http://192.168.1.115:8000/trx/coins/createcoins

se envía:
```json
{
    "ticker_symbol":"BTC",
    "ticker_name": "BITCOIN"
    
}
```

Para fondear la cuenta de airdrop (sólo admin):

http://192.168.1.115:8000/trx/fundairdrop?&amount=10&cointicker=BTC

para solicitar un airdrop(usuarios registrados):

http://192.168.1.115:8000/trx/requestairdrop?&cointicker=BTC

para quemar monedas(usuario registrados):

http://192.168.1.115:8000/trx/requestburn?&cointicker=BTC&amount=0.00001

para envío de pagos a través de p2p (usuarios registrados):

http://192.168.1.115:8000/trx/p2p?&cointicker=BTC&amount=100&wallet=0x2516533a54affb142f1490d3485db410ee5d8c21

para consultar los tickers disponibles:

http://192.168.1.115:8000/trx/coins/list

respuesta:

```json
[
    {
        "id": 1,
        "ticker_symbol": "BTC",
        "ticker_name": "BITCOIN"
    },
    {
        "id": 2,
        "ticker_symbol": "LTC",
        "ticker_name": "LITECOIN"
    },
    {
        "id": 3,
        "ticker_symbol": "USDT",
        "ticker_name": "TETHER"
    },
    {
        "id": 4,
        "ticker_symbol": "ADA",
        "ticker_name": "CARDANO"
    },
    {
        "id": 5,
        "ticker_symbol": "DOGE",
        "ticker_name": "DOGECOIN"
    },
    {
        "id": 6,
        "ticker_symbol": "ETH",
        "ticker_name": "ETHEREUM"
    },
    {
        "id": 7,
        "ticker_symbol": "SOL",
        "ticker_name": "SOLANA"
    }
]
```

las transacciones:

http://192.168.1.115:8000/trx/list

respuesta:

```json
{
        "id": 18,
        "tx_hash": "Z0FBQUFBQmlZQ0ptWm1WVVVCclVQdi1GZERmODdfa2pHaVp0Rk1icUI4UDE2VzBfb3F1cHAtcnk4Nk1sVkxlYjIxZVUwU3lyRkdRbFV2M2hYek5PSHJqZDY3RXJZVndleVJiWWpLaGZUdmZaajlvb0hpLXpaaHc9",
        "tx_type": "p2p",
        "previous_amount_from": 9.9998,
        "previous_amount_to": 0.0,
        "current_amount": 0.0004,
        "after_amount_from": 9.9994,
        "after_amount_to": 0.0004,
        "date_time": "2022-04-20T15:10:30.833022Z",
        "wallet_from": 5,
        "wallet_to": 7,
        "ticker": 1
    }
```

balances:

http://192.168.1.115:8000/trx/balances/list

respuesta:


```json
{
	    {
        "id": 4,
        "wallet": "0xd65339361a81a1fdb406e7999db4d386fe2658de",
        "coin_ticker": "TETHER",
        "deposit_date": "2022-04-20T13:32:54.640926Z",
        "last_up_date": "2022-04-20T13:40:25.103057Z",
        "amount": 99990.0
    },
    {
        "id": 5,
        "wallet": "0xd65339361a81a1fdb406e7999db4d386fe2658de",
        "coin_ticker": "DOGECOIN",
        "deposit_date": "2022-04-20T13:33:13.233330Z",
        "last_up_date": "2022-04-20T13:40:11.254227Z",
        "amount": 199990.0
    },
    {
        "id": 6,
        "wallet": "0x2516533a54affb142f1490d3485db410ee5d8c21",
        "coin_ticker": "BITCOIN",
        "deposit_date": "2022-04-20T13:40:05.051662Z",
        "last_up_date": "2022-04-20T15:10:30.908910Z",
        "amount": 0.0004
    }
}
```