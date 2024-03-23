# online_wallet

python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com

Для того, чтобы совешить транзакцию, необходимо ввести следующие данные:
username_1 - пользователь, у которого берут деньги
username_2 - пользователь, которому переводят деньги
wallet_name_1 - кошелек пользователя, у которого берут деньги
wallet_name_2 - кошелек пользователя, которому переводят деньги
transfer_money - количество денег, которые должны перевести

Например:
curl  -H 'Content-Type: application/json' --data '{"username_1":"Bob","username_2":"Tom", "wallet_name_1": "Bobs_wallet", "wallet_name_2": "Toms_wallet", "transfer_money": "2.0"}' http://127.0.0.1:8000/wallet/transfer_money/
