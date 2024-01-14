# forms.py
from django import forms
from .models import Category

class TransactionForm(forms.Form):
    TRANSACTION_CHOICES = [
        ('income', 'Дохід'),
        ('expense', 'Витрата'),
    ]

    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, widget=forms.RadioSelect)
    amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all())  # Використовуємо ModelChoiceField для вибору з існуючих категорій


class CustomPeriodForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

