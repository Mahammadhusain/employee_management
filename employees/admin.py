from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'username', 'email', 'name', 'role', 'date_of_joining', 'is_active',)
    list_filter = ('role', 'is_active', 'is_staff', 'date_of_joining')
    search_fields = ('username', 'email', 'name')
    ordering = ('date_of_joining',)

    # Fields to display on the admin detail/edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'date_of_joining', 'supervised_by')}),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display on the admin create user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'name', 'date_of_joining', 'role', 'supervised_by', 'is_active', 'is_staff'),
        }),
    )

    # Ensure supervised_by is displayed and works properly
    autocomplete_fields = ['supervised_by']  # Enable autocomplete for related fields

    # Manage permissions dynamically
    def get_fieldsets(self, request, obj=None):
        """Adjust fieldsets based on user permissions."""
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # Remove certain fields for non-superusers
            restricted_fields = ('is_superuser', 'groups', 'user_permissions')
            fieldsets = tuple(
                (title, {'fields': [field for field in opts['fields'] if field not in restricted_fields]})
                for title, opts in fieldsets
            )
        return fieldsets

    def get_queryset(self, request):
        """Restrict queryset for non-superadmins."""
        qs = super().get_queryset(request)
        if request.user.role == 'admin':
            return qs.filter(supervised_by=request.user)
        return qs
