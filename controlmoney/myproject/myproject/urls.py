from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views import AccountViewSet, ExpenseViewSet, IncomeViewSet
from users.views import register_view, login_view, logout_view, home
from transactions.views import TransactionViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finance/', include('finance.urls')),
    path('api/', include(router.urls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
]
