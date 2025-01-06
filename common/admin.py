from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'created', 'active']
    readonly_fields = ['key', 'created']
    actions = ['activate_keys', 'deactivate_keys']

    def activate_keys(self, request, queryset):
        queryset.update(active=True)

    def deactivate_keys(self, request, queryset):
        queryset.update(active=False)
