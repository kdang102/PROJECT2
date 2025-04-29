from django.contrib import admin
from .models import Service
from .models import Income, Expense

class ServiceAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Service, ServiceAdmin)
admin.site.register(Income)
admin.site.register(Expense)
