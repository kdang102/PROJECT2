from django.db.models import Sum
from .models import Income, Expense


def total_income(request):
    if not request.user.is_authenticated:
        return {'total_income': 0}

    result = Income.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Convert to float then int to handle both decimals and whole numbers
    return {'total_income': int(float(result))}


def total_expenses(request):
    if not request.user.is_authenticated:
        return {'total_expenses': 0}

    result = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return {'total_expenses': int(float(result))}


def difference(request):
    if not request.user.is_authenticated:
        return {'difference': 0}

    income = float(Income.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0)

    expenses = float(Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0)

    return {'difference': income - expenses}