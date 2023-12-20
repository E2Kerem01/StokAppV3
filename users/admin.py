from django.contrib import admin

from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_supplier']


admin.site.register(User, UserAdmin)


