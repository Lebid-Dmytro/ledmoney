# У вашому файлі urls.py

from django.urls import path
from .views import CurrentMonthStatisticsView, AddTransactionView, CustomPeriodStatisticsView

urlpatterns = [
    path('current_month/', CurrentMonthStatisticsView.as_view(), name='current_month_statistics'),
    path('add_transaction/', AddTransactionView.as_view(), name='add_transaction'),
    path('custom_period/', CustomPeriodStatisticsView.as_view(), name='custom_period_statistics'),
]
