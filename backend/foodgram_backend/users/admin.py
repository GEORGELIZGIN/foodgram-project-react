from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import UserChangeForm, UserCreationForm
from users.models import Subscription

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'email', 'username',
        'first_name', 'last_name',
        'is_superuser', 'id')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name',
                'last_name', 'username',
                'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'follower')
    list_filter = ('author__email', 'follower__email')
    search_fields = ('author__email', 'follower__email')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
