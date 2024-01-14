from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views import View
from django.utils import timezone
import calendar

from django.views.generic import FormView

from .forms import TransactionForm, CustomPeriodForm
from .models import Transaction, Category


class CurrentMonthStatisticsView(View):
    template_name = 'current_month_statistics.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        _, last_day = calendar.monthrange(today.year, today.month)
        first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = today.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)

        income = Transaction.objects.filter(user=request.user, transaction_type='income',
                                            date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = Transaction.objects.filter(user=request.user, transaction_type='expense',
                                              date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expenses

        context = {
            'income': income,
            'expenses': expenses,
            'balance': balance,
        }

        return render(request, self.template_name, context)


class AddTransactionView(View):
    template_name = 'add_transaction.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': TransactionForm(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_data = form.cleaned_data
            category, created = Category.objects.get_or_create(name=transaction_data['category'])
            Transaction.objects.create(user=request.user, category=category,
                                       transaction_type=transaction_data['transaction_type'],
                                       amount=transaction_data['amount'], date=transaction_data['date'])
            return redirect('current_month_statistics')

        return render(request, self.template_name, {'form': form})


class CustomPeriodStatisticsView(FormView):
    template_name = 'custom_period_statistics.html'
    form_class = CustomPeriodForm  # Замініть це на вашу форму для вибору періоду
    success_url = '/custom_period/'  # Можливо, слід вказати власний URL для перенаправлення

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Отримати транзакції за обраний період
        transactions = Transaction.objects.filter(
            user=self.request.user,
            date__range=[start_date, end_date],
        )

        # Підрахувати суму доходів та витрат
        income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expenses

        context = {
            'start_date': start_date,
            'end_date': end_date,
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'form': form,
        }

        return self.render_to_response(context)