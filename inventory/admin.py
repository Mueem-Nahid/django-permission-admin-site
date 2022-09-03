from .models import Product
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Unregistering user and group (default) | Restricting default access for super users
admin.site.unregister(User)

# Register your models here.


# Overriding
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['username'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        return form


# admin.site.register(Product)  # to show inventory in admin site
class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.has_perm('inventory.change_product'):
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('inventory.delete_product'):
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        return True


# To override
@admin.register(Product)
class ProductAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("name",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['web_id'].disabled = True
        return form
