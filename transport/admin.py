from django.contrib import admin
from django.contrib.auth.models import Group
from transport.models import Provider, ServiceArea


admin.site.unregister(Group)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',
                    'language', 'currency',
                    'created_at', 'updated_at')


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',
                    'created_at', 'updated_at')
