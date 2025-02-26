from django.contrib import admin
from .models import Products, Employees, Departments, Orders


admin.site.register(Departments)
admin.site.register(Employees)
admin.site.register(Orders)
admin.site.register(Products)
