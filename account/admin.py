from django.contrib import admin

from .models import Customer

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'name', 'email')
    search_fields = ('username', 'email')
    list_filter = ('is_superuser',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        ('User', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'mobile', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )