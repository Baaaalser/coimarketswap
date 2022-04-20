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