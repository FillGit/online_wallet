from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Wallet(models.Model):
    CURRENCY = (
        ('RUB', 'RUB'),
        ('USD', 'USD'),
    )

    wallet_name = models.CharField(max_length=25, blank=False)
    currency = models.CharField(max_length=3, blank=False, choices=CURRENCY)
    money = models.FloatField(default=10, blank=False,
                              validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    user_obj = models.ForeignKey(User,
                                 on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['wallet_name', 'user_obj'],
                name='not unique wallet_name and user_obj')
        ]


class WalletCard(models.Model):
    wallet_obj = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    changed = models.DateTimeField(auto_now_add=True)
    min_max = models.CharField(max_length=25, blank=False)
