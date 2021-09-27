from Users.models import CustomUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import datetime as dt
import random
# Create your models here.

class BaseEntity(models.Model):
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f'[MODEL] {self.user} ---wallet-id--> {self.id}'

class Transaction(BaseEntity):
    '''Money Transaction'''
    TRNSACTION_TYPE = (
        ('MERCHANT_INCOME', 'MERCHANT_INCOME'),
        ('SERVICE_OUTCOME', 'SERVICE_OUTCOME'),
        ('USER_2_USER_OUTCOME', 'USER_2_USER_OUTCOME'),
        ('USER_2_USER_INCOME', 'SERVICE_INCOME'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    amount = models.DecimalField(_('Amount of transaction'), max_digits=10, decimal_places=2)
    transaction_from = models.CharField(_('Transaction action from - wallet id,merchant,service'), max_length=50, blank=False, null=True)
    transaction_to = models.CharField(_('Transaction action from - wallet id,merchant,service'), max_length=50, blank=False, null=True)
    transaction_type = models.CharField(_('Transaction Type'), max_length=20, choices=TRNSACTION_TYPE, blank=False)

    wallets = models.ManyToManyField(Wallet, verbose_name=_('Wallet'), blank=False, related_name='transactions')

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f'[MODEL] {self.wallets} ---transaction--> id:{self.id}, type:{self.transaction_type}, amount:{self.amount}'