from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Income, Expense, Budget
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, openai
from django.conf import settings

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        services = Service.objects.filter(name__icontains=search_term)
    else:
        services = Service.objects.all()
    template_data = {}
    template_data['title'] = 'services'
    template_data['services'] = services
    return render(request, 'services/index.html',
                  {'template_data': template_data})
def show(request, id):
    service = Service.objects.get(id=id)
    template_data = {}
    template_data['title'] = service.name
    template_data['service'] = service
    return render(request, 'services/show.html',
                  {'template_data': template_data})


@login_required
def add_income(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date_added')
    total_income = sum(income.amount for income in incomes)

    if request.method == 'POST':
        try:
            amount = request.POST.get('income_amount')
            if float(amount) <= 0:
                messages.error(request, 'Income amount must be positive')
            else:
                Income.objects.create(user=request.user, amount=amount)
                messages.success(request, 'Income saved successfully!')
                return redirect('add_income')  # Refresh the page
        except ValueError:
            messages.error(request, 'Please enter a valid number')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'services/add_income.html', {
        'incomes': incomes,
        'total_income': total_income
    })


@login_required
def income_report(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date_added')
    total_income = sum(income.amount for income in incomes)

    return render(request, 'services/income_report.html', {
        'incomes': incomes,
        'total_income': total_income
    })


@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income record deleted successfully!')
    return redirect('add_income')

# expenses
@login_required
def add_expense(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date_added')
    total_expenses = sum(expense.amount for expense in expenses)

    if request.method == 'POST':
        try:
            description = request.POST.get('expense_description')
            amount = request.POST.get('expense_amount')
            if float(amount) <= 0:
                messages.error(request, 'Your spending must be positive! If you want to add income, go back.')
            elif description == '':
                messages.error(request, 'Description cannot be empty!')
            else:
                Expense.objects.create(user=request.user, amount=amount, description=description)
                messages.success(request, 'Spending saved successfully!')
                return redirect('add_expense')  # Refresh the page
        except ValueError:
            messages.error(request, 'Please enter a valid number')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'services/add_expense.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })

# expenses
@login_required
def add_budget(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-date_added')
    total_budgets = sum(budget.limit_amount for budget in budgets)

    if request.method == 'POST':
        try:
            category = request.POST.get('budget_category')
            limit_amount = request.POST.get('budget_limit_amount')
            if float(limit_amount) <= 0:
                messages.error(request, 'Your spending cannot be negative! If you want to add income, go back.')
            elif category == '':
                messages.error(request, 'Category cannot be empty!')
            else:
                Budget.objects.create(user=request.user, limit_amount=limit_amount, category=category)
                messages.success(request, 'Spending saved successfully!')
                return redirect('add_budget')  # Refresh the page
        except ValueError:
            messages.error(request, 'Please enter a valid number')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'services/add_budget.html', {
        'budgets': budgets,
        'total_budgets': total_budgets
    })

@login_required
def expense_report(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date_added')
    total_expenses = sum(expense.amount for expense in expenses)

    return render(request, 'services/expense_report.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense record deleted successfully!')
    return redirect('add_expense')


@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Spending limit deleted successfully!')
    return redirect('add_budget')


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        try:
            description = request.POST.get('expense_description')
            amount = request.POST.get('expense_amount')
            if float(amount) <= 0:
                messages.error(request, 'Your spending must be positive! If you want to add income, go back.')
            elif description == '':
                messages.error(request, 'Description cannot be empty!')
            else:
                expense.description = description
                expense.amount = amount
                expense.save()
                messages.success(request, 'Spending saved successfully!')
                return redirect('add_expense')
        except ValueError:
            messages.error(request, 'Please enter a valid number')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    expenses = Expense.objects.filter(user=request.user).order_by('-date_added')
    total_expenses = sum(expense.amount for expense in expenses)

    return render(request, 'services/edit_expense.html', {
        'expenses': expense,
        'total_expenses': total_expenses
    })


@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)

    if request.method == 'POST':
        try:
            category = request.POST.get('budget_category')
            limit_amount = str(request.POST.get('budget_limit_amount'))
            if not limit_amount and float(limit_amount) < 0:
                messages.error(request, 'Your spending limit can\'t be negative! If you want to add income, go back.')
            elif category == '':
                messages.error(request, 'Category cannot be empty!')
            else:
                budget.category = category
                budget.limit_amount = limit_amount
                budget.save()
                messages.success(request, 'Budget saved successfully!')
                return redirect('add_budget')
        except ValueError as v:
            #messages.error(request, limit_amount)
            #messages.error(request, f'Error: {v}')
            #messages.error(request, 'Please enter a valid number')
            limit_amount = 0
        except Exception as e:
            #messages.error(request, 'Helpp')
            #messages.error(request, f'Error: {e}')
            limit_amount = 0

    budgets = Budget.objects.filter(user=request.user).order_by('-date_added')
    total_budgets = sum(budget.limit_amount for budget in budgets)

    return render(request, 'services/edit_budget.html', {
        'budgets': budget,
        'total_budgets': total_budgets
    })
@login_required
def chart_dashboard(request):
    return render(request, 'services/chart.html')


@login_required
def income_summary(request):
    incomes = Income.objects.filter(user=request.user)
    if incomes.exists():
        labels = [f"Income {idx}" for idx, _ in enumerate(incomes, start=1)]
        data = [float(income.amount) for income in incomes]
    else:
        labels = ["No income data"]
        data = [0]

    return JsonResponse({
        'labels': labels,
        'data': data
    })


@login_required
def spending_summary(request):
    spendings = Expense.objects.filter(user=request.user)
    if spendings.exists():
        summary = {}
        for spending in spendings:
            if spending.description not in summary:
                summary[spending.description] = 0
            summary[spending.description] += float(spending.amount)
        labels = list(summary.keys())
        data = list(summary.values())
    else:
        labels = ["No spending data"]
        data = [0]

    return JsonResponse({
        'labels': labels,
        'data': data
    })

@login_required
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)

    if request.method == 'POST':
        try:
            amount = request.POST.get('income_amount')
            if not amount or float(amount) <= 0:
                messages.error(request, 'Income amount must be positive!')
            else:
                income.amount = amount
                income.save()
                messages.success(request, 'Income updated successfully!')
                return redirect('add_income')
        except ValueError:
            messages.error(request, 'Please enter a valid number.')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    incomes = Income.objects.filter(user=request.user).order_by('-date_added')
    total_income = sum(income.amount for income in incomes)

    return render(request, 'services/edit_income.html', {
        'incomes': income,
        'total_income': total_income
    })

@login_required
def chatbot_page(request):
    return render(request, 'services/chatbot.html')

@csrf_exempt
@login_required
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')
        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for finance tracking and budgeting."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message['content'].strip()
            return JsonResponse({'response': answer})
        except Exception as e:
            return JsonResponse({'response': f"Error: {str(e)}"})

    return JsonResponse({'error': 'Invalid request'}, status=400)