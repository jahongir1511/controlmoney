from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, ExpenseForm
from .models import Account, Expense, Income
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from .serializers import AccountSerializer, ExpenseSerializer, IncomeSerializer
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def login(request):
    return HttpResponse("Login Page")

def register(request):
    return HttpResponse("Register Page")

def dashboard(request):
    return HttpResponse("Dashboard Page")


@login_required(login_url='/login/')
def dashboard(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expenses

    monthly_income = Income.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_expenses = Expense.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_income = Income.objects.filter(date__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_expenses = Expense.objects.filter(date__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or 0

    recent_incomes = Income.objects.order_by('-date')[:5]
    recent_expenses = Expense.objects.order_by('-date')[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'yearly_income': yearly_income,
        'yearly_expenses': yearly_expenses,
        'recent_incomes': recent_incomes,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def finance_home(request):
    if request.method == 'POST':
        if 'add_income' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income_form.save()
                return redirect('finance_home')
        elif 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense_form.save()
                return redirect('finance_home')
    else:
        income_form = IncomeForm()
        expense_form = ExpenseForm()

    accounts = Account.objects.all()
    expenses = Expense.objects.all()
    incomes = Income.objects.all()

    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    weekly_expenses = Expense.objects.filter(date__gte=start_of_week).aggregate(Sum('amount'))
    monthly_expenses = Expense.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))
    yearly_expenses = Expense.objects.filter(date__gte=start_of_year).aggregate(Sum('amount'))

    weekly_incomes = Income.objects.filter(date__gte=start_of_week).aggregate(Sum('amount'))
    monthly_incomes = Income.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))
    yearly_incomes = Income.objects.filter(date__gte=start_of_year).aggregate(Sum('amount'))

    context = {
        'accounts': accounts,
        'expenses': expenses,
        'incomes': incomes,
        'income_form': income_form,
        'expense_form': expense_form,
        'weekly_expenses': weekly_expenses,
        'monthly_expenses': monthly_expenses,
        'yearly_expenses': yearly_expenses,
        'weekly_incomes': weekly_incomes,
        'monthly_incomes': monthly_incomes,
        'yearly_incomes': yearly_incomes,
    }
    return render(request, 'home.html', context)

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance_home')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance_home')
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
