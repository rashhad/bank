from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from .forms import signUpForm, ChangeUserForm,ChangeUserInfoForm, depositForm, withdrawForm, loanForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from . import models
from datetime import date
from django.contrib import messages
from time import sleep

# Create your views here.

class home(TemplateView):
    template_name = 'home.html'

class sign_up(FormView):
    template_name= 'register.html'
    form_class=signUpForm
    success_url='/login/'

    def form_valid(self, form) -> HttpResponse:
        form.save()
        return super().form_valid(form)

class loginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class logoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')

def profile(request):
    if request.method=='POST':
        formA=ChangeUserForm(data=request.POST)
        formB=ChangeUserInfoForm(data=request.POST)
        if formA.is_valid() and formB.is_valid():
            formA.save(request)
            formB.save(request)
            return render(request, './profile.html', {'formA':formA, 'formB':formB})
    dataA=models.User.objects.get(id=request.user.id)
    dataB=models.UserInfo.objects.get(user=request.user.id)
    formA=ChangeUserForm(instance=dataA)
    formB=ChangeUserInfoForm(instance=dataB)
    return render(request, './profile.html', {'formA':formA, 'formB':formB})


def withdraw(request):
    if request.method=='POST':
        form = withdrawForm(request.POST)
        if form.is_valid():
            form.withdraw(request)
            return redirect('withdraw')
    else:
        form=withdrawForm()
    return redirect('statement')

def deposit(request):
    if request.method=='POST':
        form = depositForm(request.POST or None)
        if form.is_valid():
            form.deposit(request)
            return redirect('deposit')
    else:
        form=depositForm()
    return redirect('statement')

def Statement(request):
    if request.method=='POST':
        stdt=request.POST['startDate']
        endt=request.POST['endDate']
        if stdt=='':
            stdt=date.today()
        if endt=='':
            endt=date.today()
        print(date.today())
        statement_data=models.statement.objects.filter(date__lte=endt,date__gte=stdt)
    else:
        statement_data=models.statement.objects.filter(user=request.user.id)
    bal=models.UserInfo.objects.get(user=request.user.id).balance
    return render(request, './statement.html',{'data':statement_data, 'balance':bal})

def loanPage(request):
    loan_data=models.loan.objects.filter(user=request.user.id)
    return render(request, './loan.html',{'data':loan_data})

def loanDisposal(request, id):
    if request.method=='GET':
        if 'loanStatus' in request.GET:
            if request.GET['loanStatus']=='Approved':
                models.loan.objects.filter(id=id).update(dateOfDisposal=date.today())
                models.loan.objects.filter(id=id).update(status='Approved')
                cur_bal=models.UserInfo.objects.get(user=request.user.id).balance
                cur_bal+=models.loan.objects.get(id=id).amount
                models.UserInfo.objects.filter(user=request.user.id).update(balance=cur_bal)
                
                models.statement.objects.create(
                    detail='Loan Approved',
                    credit=models.loan.objects.get(id=id).amount,
                    debit=0,
                    transactionType="Loan",
                    user=request.user,
                )
            else:
                models.loan.objects.filter(id=id).update(status='Denied')
                models.loan.objects.filter(id=id).update(dateOfDisposal=date.today())
        else: #pay
            cur_bal=models.UserInfo.objects.get(user=request.user.id).balance
            paid_amount=models.loan.objects.get(id=id).amount
            if cur_bal>=paid_amount:
                cur_bal-=paid_amount
                models.UserInfo.objects.filter(user=request.user.id).update(balance=cur_bal)
                models.loan.objects.filter(id=id).update(status='Paid')
                models.statement.objects.create(
                detail='Loan Paid',
                credit=0,
                debit=models.loan.objects.get(id=id).amount,
                transactionType="Loan",
                user=request.user,
            )
                messages.add_message(request,messages.SUCCESS,'Thank You!')
            else:
                messages.add_message(request,messages.INFO,'Insufficient Balance')
    return redirect('loan')

def applyLoan(request):
    if request.method=='POST':
        form=loanForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('loan')
        form=loanForm(request.POST)
        return render(request, './loanForm.html',{'form':form})
    form=loanForm()
    return render(request, './loanForm.html',{'form':form})