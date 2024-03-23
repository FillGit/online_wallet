from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from wallet_app.app.models import Wallet
from wallet_app.app.serializers import TransferMoneySerializer


class WalletViewSet(ModelViewSet):

    def check_currency(self, wallet_1_obj, wallet_2_obj):
        if wallet_1_obj.currency != wallet_2_obj.currency:
            return True

    def check_transfer(self, wallet_1_obj, transfer_money):
        if (wallet_1_obj.money - transfer_money) < 0:
            return True

    def _transfer_money(self, wallet_1_obj, wallet_2_obj,
                        transfer_money):
        wallet_1_obj.money = wallet_1_obj.money - transfer_money
        wallet_2_obj.money = wallet_2_obj.money + transfer_money
        Wallet.objects.bulk_update([wallet_1_obj, wallet_2_obj],
                                   ["money", "money"])
        wallet_1_obj.walletcard_set.create(
            min_max=f' - {transfer_money} {wallet_1_obj.currency}')
        wallet_2_obj.walletcard_set.create(
            min_max=f' + {transfer_money} {wallet_2_obj.currency}')

    @action(detail=False, url_path='transfer_money', methods=['post'])
    def transfer_money(self, request, pk=None):
        serializer = TransferMoneySerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        username_1 = request.data['username_1']
        username_2 = request.data['username_2']
        wallet_name_1 = request.data['wallet_name_1']
        wallet_name_2 = request.data['wallet_name_2']
        transfer_money = request.data['transfer_money']
        try:
            wallet_1_obj = Wallet.objects.get(user_obj__username=username_1,
                                              wallet_name=wallet_name_1)
            wallet_2_obj = Wallet.objects.get(user_obj__username=username_2,
                                              wallet_name=wallet_name_2)
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        if self.check_currency(wallet_1_obj, wallet_2_obj):
            return Response('different currencies',
                            status=status.HTTP_400_BAD_REQUEST)

        if self.check_transfer(wallet_1_obj, transfer_money):
            return Response(
                'The first wallet is smaller than the transfer_money',
                status=status.HTTP_400_BAD_REQUEST)
        self._transfer_money(wallet_1_obj, wallet_2_obj, transfer_money)
        return Response([], status=status.HTTP_201_CREATED)
