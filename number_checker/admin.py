from django.contrib import admin
from .models import PhoneNumber, QueryHistory

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('full_number', 'operator', 'region')
    search_fields = ('full_number', 'operator', 'region')
    list_filter = ('operator', 'region')

@admin.register(QueryHistory)
class QueryHistoryAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user', 'query_date', 'ip_address')
    list_filter = ('query_date', 'user')
    search_fields = ('phone_number__full_number', 'user__username')
    date_hierarchy = 'query_date'