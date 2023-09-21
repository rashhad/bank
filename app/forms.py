from typing import Any
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from . import choice
from django.core.exceptions import ValidationError

class signUpForm(UserCreationForm):
    gender=forms.ChoiceField(choices=choice.GENDER)
    dob=forms.DateField(label='Date of Birth')
    acc_type=forms.ChoiceField(choices=choice.ACC_TYPE, label='Account Type')
    address=forms.CharField(max_length=100,widget=forms.TextInput)

    class Meta:
        model=User
        fields=['username', 'password1','password2', 'first_name', 'last_name','email']

    def save(self, commit=True) -> Any:
        user=super().save(commit=False)
        if commit==True:
            user.save()

            user_data=self.cleaned_data
            models.UserInfo.objects.create(
                user=user,
                account_no=1000000+user.id,
                account_type=user_data['acc_type'],
                gender=user_data['gender'],
                dob=user_data['dob'],
                address=user_data['address'],
            )
        return user
    
class loginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput, max_length=50, required=True)


class ChangeUserForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def save(self, request, commit=True):
        if commit==True:
            first_name=self.cleaned_data['first_name']
            last_name=self.cleaned_data['last_name']
            email=self.cleaned_data['email']
            User.objects.filter(id=request.user.id).update(first_name=first_name, last_name=last_name, email=email)
        return request
    

class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model=models.UserInfo
        fields=['gender','dob','address']

    def save(self, request, commit=True):
        if commit==True:
            gender=self.cleaned_data['gender']
            dob=self.cleaned_data['dob']
            address=self.cleaned_data['address']
            models.UserInfo.objects.filter(user=request.user.id).update(gender=gender,dob=dob,address=address)
        return request
    
class depositForm(forms.Form):
    amount=forms.DecimalField(required=True)

    def deposit(self, request):
        models.statement.objects.create(
            detail='Direct Deposit',
            debit=0.00,
            credit=self.cleaned_data['amount'],
            transactionType="Deposite",
            user=models.User.objects.get(id= request.user.id),
        )
        cur_bal=models.UserInfo.objects.get(user=request.user.id).balance
        cur_bal+=self.cleaned_data['amount']
        models.UserInfo.objects.filter(user=request.user.id).update(balance=cur_bal)

        
class withdrawForm(forms.Form):
    amount=forms.DecimalField(required=True)

    def withdraw(self, request):
        cur_bal=models.UserInfo.objects.get(user=request.user.id).balance
        if cur_bal>=self.cleaned_data['amount']:
            cur_bal-=self.cleaned_data['amount']
            models.UserInfo.objects.filter(user=request.user.id).update(balance=cur_bal)
            models.statement.objects.create(
                detail='Direct Withdraw',
                debit=self.cleaned_data['amount'],
                credit=0,
                transactionType="Withdrwal",
                user=models.User.objects.get(id= request.user.id),
            )
        else:
            return ValidationError('Error! Insufficient balance!')
        
class loanForm(forms.Form):
    amount=forms.DecimalField()

    def save(self, request):
        user=request.user
        models.loan.objects.create(
            user=user,
            status='Pending',
            amount=self.cleaned_data['amount']
        )
