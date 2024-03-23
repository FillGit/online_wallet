from rest_framework import serializers


class TransferMoneySerializer(serializers.Serializer):
    username_1 = serializers.CharField(max_length=15)
    username_2 = serializers.CharField(max_length=15)
    wallet_name_1 = serializers.CharField(max_length=15)
    wallet_name_2 = serializers.CharField(max_length=15)
    transfer_money = serializers.FloatField()
