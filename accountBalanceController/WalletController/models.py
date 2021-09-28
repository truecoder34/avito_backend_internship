from django.core.exceptions import ValidationError
from Users.models import CustomUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import datetime as dt
import random
# Create your models here.

class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    modify_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "Base Entity"
        verbose_name_plural = "Base Entities"

class Wallet(BaseEntity):
    ''' Wallet '''
    number_walet = models.CharField(_("Number of wallet"), max_length=20, unique=True, null=True, blank=True)
    balance = models.DecimalField(_('Balance'), decimal_places=2, max_digits=10, default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('User'), related_name='wallets')

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f'[MODEL] {self.user} ---wallet-id--> {self.id}'

class MerchantOuter(BaseEntity):
    '''Money Income from Merchant'''
    YEARS = [
        (str(year), str(year),)
        for year in range(dt.datetime.now().year, dt.datetime.now().year + 5)
    ]
    MONTH = (
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    )
    MERCHANT_TYPE = (
        ('VISA', 'VISA'),
        ('MS', 'MS')
    )
    number = models.CharField(_('Card number'), max_length=20)
    merchant_type = models.CharField(_('Merchant type'), max_length=10)
    year = models.CharField(_('Year'), max_length=4,   choices=YEARS, default=dt.datetime.now().year)
    month = models.CharField(_('Month'), max_length=8, choices=MONTH, default=dt.datetime.now().month)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name=_('Wallet'), related_name='MerchantOuter')
    #date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'

    def __str__(self):
        return (
            f'[MODEL] Income #{self.id} on amont: {self.amount}. '
            f'By user: {self.wallet.user}'
        )


class Service(BaseEntity):
    '''
    SERVICES PRESENTED
    [ACCESS] : only by Admin
    '''
    CUREENCY = (
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('EUR', 'EUR')
    )
    name = models.CharField(_('Name of service'), max_length=63)
    description = models.TextField(_('Description'))
    cost = models.DecimalField(_('Cost of service'), max_digits=10, decimal_places=2)
        # validators=[
        #     DecimalValidator(max_digits=10, decimal_places=2),
        #     price_less_than_one
        # ])
    currency = models.CharField(_('Currency'), choices=CUREENCY, default="RUB", max_length=6)
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f'{self.name}'

    def validate_price(self, cost):
        if cost < 1:
            raise ValidationError('Cost of service should be > 1')
        return cost

class ServiceTransaction(BaseEntity):
    ''' storage of bought services'''
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='service_transactions', verbose_name=_('Wallet'))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_transaction', verbose_name=_('Service'))

    class Meta:
        verbose_name = 'Service buy'
        verbose_name_plural = 'Services buy'
        ordering = ['-create_datetime']

    def __str__(self):
        return (
            f"[MODEL] from {self.wallet} wallet bought service {self.service.name} "
            f"for {self.service.cost}"
        )


class MoneyTransfer(BaseEntity):
    wallet_send = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        verbose_name=_("Sender's wallet"),
        related_name='money_send'
    )
    wallet_received = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        verbose_name=_('Sender received'),
        related_name='money_received'
    )
    amount = models.DecimalField(_('Сумма'), max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return (
            f"{self.wallet_send} -> {self.wallet_received} ({self.amount}) at {self.create_datetime}"
        )