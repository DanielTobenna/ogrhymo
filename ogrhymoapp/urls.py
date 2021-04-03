from django.urls import path

from . import views

urlpatterns=[
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('promotion/', views.promotion, name='promotion'),
	path('signup/', views.signup, name='signup'),
	path('loginpage/', views.loginpage, name='loginpage'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('deposite/', views.deposite, name='deposite'),
	path('account_settings/', views.accountSettings, name='account_settings'),
	path('requestwithdrawal/', views.requestwithdrawal, name='requestwithdrawal'),
	path('logout/', views.logoutuser, name='logout'),
]