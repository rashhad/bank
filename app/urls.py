from django.urls import path
from . import views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('profile/', views.profile, name='profile'),
    path('sign_up/', views.sign_up.as_view(), name='sign_up'),
    path('statement/', views.Statement, name='statement'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('loan/', views.loanPage, name='loan'),
    path('loan/<int:id>', views.loanDisposal, name='loanDis'),
    path('apply/', views.applyLoan, name='applyLoan'),
]
