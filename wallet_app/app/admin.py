from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from wallet_app.app.models import Wallet, WalletCard

admin.site.unregister(User)


@admin.register(WalletCard)
class WalletCardAdmin(admin.ModelAdmin):
    list_display = ('min_max', 'changed')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_name', 'user_obj', 'currency', 'money', 'created',
                    'walletcard_link')

    def walletcard_link(self, obj):
        count = obj.walletcard_set.count()
        url = (
            reverse('admin:app_walletcard_changelist')
            + '?'
            + urlencode({'wallet_obj__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} wallet card</a>', url, count)

    walletcard_link.short_description = 'wallet_card'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'wallet_link')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )

    def wallet_link(self, obj):
        count = obj.wallet_set.count()
        url = (
            reverse('admin:app_wallet_changelist')
            + '?'
            + urlencode({'user_obj__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} wallet</a>', url, count)

    wallet_link.short_description = 'wallet'
