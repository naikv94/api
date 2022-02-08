from django.contrib import admin
from .models import Company,Contact


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['uid','name','country','contact']
    search_fields = ['name','country']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','phone','company']
    search_fields = ['name','company__name']
