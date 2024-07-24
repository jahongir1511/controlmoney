from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.finance_home, name='finance_home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
