from django.db import models
from django.contrib.auth.models import User
from . import choice

# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    account_no=models.IntegerField(unique=True)
    account_type = models.CharField(max_length=10, choices=choice.ACC_TYPE)
    gender = models.CharField(max_length=6, choices=choice.GENDER)
    dob=models.DateField()
    address = models.TextField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    totalLoan = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.account_no} bal: {self.balance}'
    
class statement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statement')
    date = models.DateTimeField(auto_now_add=True)
    transactionType = models.CharField(max_length=10, choices=choice.TX_TYPE)
    detail = models.TextField(null=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit= models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        if self.credit:
            val=self.credit
        else:
            val=self.debit
        return f'{self.user.first_name}-{val}-{self.transactionType}'

class loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan')
    dateOfApplication = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=choice.LOAN_STATUS)
    dateOfDisposal = models.DateTimeField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
