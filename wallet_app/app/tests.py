from django_webtest import WebTest
from django.contrib.auth.models import User
from hamcrest import assert_that, is_, calling, raises
from webtest.app import AppError

from wallet_app.app.models import Wallet, WalletCard


class TransferMoneyTest(WebTest):

    def set_items_db(self):
        Wallet.objects.bulk_create(
            [Wallet(user_obj=User.objects.create(username='Bob'),
                    currency='RUB',
                    wallet_name='Bobs_wallet'),
             Wallet(user_obj=User.objects.create(username='Tom'),
                    currency='RUB',
                    wallet_name='Toms_wallet'),
             Wallet(user_obj=User.objects.create(username='John'),
                    currency='USD',
                    wallet_name='John_wallet'),
             ]
        )

    def test_happy_path(self):
        self.set_items_db()
        params = {'username_1': 'Bob',
                  'username_2': 'Tom',
                  'wallet_name_1': 'Bobs_wallet',
                  'wallet_name_2': 'Toms_wallet',
                  'transfer_money': 2.0
                  }
        resp = self.app.post_json('/wallet/transfer_money/', params=params)
        assert_that(resp.status_code, is_(201))
        assert_that(resp.json, is_([]))
        wcard_1 = WalletCard.objects.get(wallet_obj__wallet_name='Bobs_wallet')
        wcard_2 = WalletCard.objects.get(wallet_obj__wallet_name='Toms_wallet')
        assert_that(wcard_1.min_max, is_(' - 2.0 RUB'))
        assert_that(wcard_2.min_max, is_(' + 2.0 RUB'))

    def test_different_currencies(self):
        self.set_items_db()
        params = {'username_1': 'Bob',
                  'username_2': 'John',
                  'wallet_name_1': 'Bobs_wallet',
                  'wallet_name_2': 'John_wallet',
                  'transfer_money': 2.0
                  }
        assert_that(calling(self.app.post).with_args(
            '/wallet/transfer_money/',
            params=params),
            raises(AppError))

    def test_first_wallet_is_smaller(self):
        self.set_items_db()
        params = {'username_1': 'Bob',
                  'username_2': 'Tom',
                  'wallet_name_1': 'Bobs_wallet',
                  'wallet_name_2': 'Toms_wallet',
                  'transfer_money': 15.0
                  }
        assert_that(
            calling(self.app.post_json).with_args(
                '/wallet/transfer_money/',
                params=params),
            raises(AppError))

    def test_empty_params(self):
        self.set_items_db()
        params = {}
        assert_that(
            calling(self.app.post_json).with_args(
                '/wallet/transfer_money/',
                params=params),
            raises(AppError))
