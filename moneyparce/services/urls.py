from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='services.index'),
    path('<int:id>/', views.show, name='services.show'),
    path('add-income/', views.add_income, name='add_income'),
    path('delete-income/<int:income_id>/', views.delete_income, name='delete_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('delete-expense/<int:expense_id>', views.delete_expense, name='delete_expense'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('add-budget/', views.add_budget, name='add_budget'),
    path('delete-budget/<int:budget_id>', views.delete_budget, name='delete_budget'),
    path('edit-budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('api/income_summary/', views.income_summary, name='income_summary'),
    path('api/spending_summary/', views.spending_summary, name='expense_summary'),
    path('chart/', views.chart_dashboard, name='services.chart_dashboard'),
    path('edit_income/<int:income_id>/', views.edit_income, name='edit_income'),
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),

]