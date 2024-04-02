from django.contrib import admin

# Register your models here.
from .models import currency_data

admin.site.register(currency_data)