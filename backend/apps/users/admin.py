from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'username', 'first_name',)
    list_filter = ('email', 'first_name',)
    fieldsets = (
        ('Регистрационные данные', {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('username',
                                                'first_name',
                                                'last_name')}),
        ('Права доступа', {'fields': ('is_superuser',
                                      'is_staff',
                                      'is_active',
                                      'groups',
                                      'user_permissions',)}),
        ('Даты регистрации и входа', {'fields': ('last_login',
                                                 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'username',
                       'first_name',
                       'last_name',
                       'password1',
                       'password2'),
        }),
    )
    search_fields = ('email', 'name', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
