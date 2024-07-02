from django.contrib import admin
from .models import TestPackage

class TestPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'date_ordered')

admin.site.register(TestPackage, TestPackageAdmin)
